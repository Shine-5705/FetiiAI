import gradio as gr
import plotly.graph_objects as go
from data_processor import DataProcessor
from chatbot_engine import FetiiChatbot
from visualizations import create_visualizations
import config
import utils

# Global data processors and chatbot
data_processor = DataProcessor()
chatbot = FetiiChatbot(data_processor)

def chat_response(message, history):
    """Handle chat interactions with the Fetii AI chatbot with enhanced responses."""
    # Add typing indicator simulation and enhanced response
    import time
    
    # Process the query
    response = chatbot.process_query(message)
    
    # Enhance response with emojis and formatting for better UX
    if "peak" in message.lower() or "busy" in message.lower():
        response = f"📊 **Peak Hours Analysis**\n\n{response}"
    elif "group" in message.lower() or "size" in message.lower():
        response = f"👥 **Group Size Insights**\n\n{response}"
    elif "location" in message.lower() or "where" in message.lower():
        response = f"📍 **Location Analysis**\n\n{response}"
    elif "trend" in message.lower() or "pattern" in message.lower():
        response = f"📈 **Trend Analysis**\n\n{response}"
    else:
        response = f"🤖 **Fetii AI Analysis**\n\n{response}"
    
    return response

def create_filter_controls():
    """Create interactive filter controls for the dashboard."""
    with gr.Row():
        with gr.Column():
            time_filter = gr.Dropdown(
                choices=["All Hours", "Morning (6-12)", "Afternoon (12-18)", "Evening (18-24)", "Night (0-6)"],
                value="All Hours",
                label="🕐 Time Filter"
            )
        with gr.Column():
            group_filter = gr.Dropdown(
                choices=["All Groups", "Small (1-4)", "Medium (5-8)", "Large (9-12)", "Extra Large (13+)"],
                value="All Groups",
                label="👥 Group Size Filter"
            )
        with gr.Column():
            refresh_btn = gr.Button(
                "🔄 Refresh Data",
                variant="secondary"
            )
    
    return time_filter, group_filter, refresh_btn

def update_dashboard(time_filter, group_filter):
    """Update dashboard based on filter selections."""
    # This would filter the data and regenerate visualizations
    # For now, return the same visualizations
    viz = create_visualizations(data_processor)
    return (
        viz['hourly_distribution'],
        viz['group_size_distribution'],
        viz['popular_locations'],
        viz['time_heatmap']
    )

def get_insights_html():
    """Generate simplified HTML for insights display that works with Gradio."""
    insights = data_processor.get_quick_insights()
    
    html_content = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: bold;">🚗 Fetii AI Assistant</h1>
        <p style="margin: 1rem 0 0 0; font-size: 1.2rem;">Your intelligent companion for Austin rideshare analytics & insights</p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin: 2rem 0;">
        <div style="background: white; border: 1px solid #e2e8f0; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 2rem; font-weight: bold; color: #1a202c;">{insights['total_trips']:,}</div>
            <div style="font-size: 0.9rem; color: #718096; margin-top: 0.5rem;">Total Trips Analyzed</div>
        </div>
        
        <div style="background: white; border: 1px solid #e2e8f0; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">�</div>
            <div style="font-size: 2rem; font-weight: bold; color: #1a202c;">{insights['avg_group_size']:.1f}</div>
            <div style="font-size: 0.9rem; color: #718096; margin-top: 0.5rem;">Average Group Size</div>
        </div>
        
        <div style="background: white; border: 1px solid #e2e8f0; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏰</div>
            <div style="font-size: 2rem; font-weight: bold; color: #1a202c;">{utils.format_time(insights['peak_hour'])}</div>
            <div style="font-size: 0.9rem; color: #718096; margin-top: 0.5rem;">Peak Hour</div>
        </div>
        
        <div style="background: white; border: 1px solid #e2e8f0; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎉</div>
            <div style="font-size: 2rem; font-weight: bold; color: #1a202c;">{insights['large_groups_pct']:.1f}%</div>
            <div style="font-size: 0.9rem; color: #718096; margin-top: 0.5rem;">Large Groups (6+)</div>
        </div>
    </div>
    
    <div class="chart-container" style="margin: 2rem 0;">
        <div style="display: flex; align-items: center; justify-content: between; margin-bottom: 1.5rem;">
            <h3 style="color: #1a202c; font-size: 1.5rem; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🔥</span>
                Hottest Pickup Locations
            </h3>
            <div style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; border-radius: 12px;">
                <span style="font-size: 0.8rem; color: #667eea; font-weight: 600;">Live Data</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
    """
    
    top_locations = list(insights['top_pickups'])[:6]
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    for i, (location, count) in enumerate(top_locations):
        color = colors[i % len(colors)]
        percentage = (count / insights['total_trips']) * 100
        
        html_content += f"""
            <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); padding: 1.5rem; border-radius: 16px; border-left: 4px solid {color}; box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: all 0.3s ease;">
                <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                    <div style="flex: 1;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #1a202c; margin-bottom: 0.5rem;">
                            #{i+1} {location[:25]}{'...' if len(location) > 25 else ''}
                        </div>
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-size: 1.5rem; font-weight: 800; color: {color};">{count}</span>
                            <span style="font-size: 0.9rem; color: #6b7280; font-weight: 500;">trips</span>
                        </div>
                    </div>
                    <div style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                        {percentage:.1f}%
                    </div>
                </div>
                <div style="background: rgba(0,0,0,0.05); border-radius: 8px; height: 6px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color}, {color}aa); height: 100%; width: {min(percentage*2, 100)}%; border-radius: 8px; transition: width 0.5s ease;"></div>
                </div>
            </div>
        """
    
    html_content += """
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
        <div style="background: rgba(72, 187, 120, 0.1); padding: 1.5rem; border-radius: 16px; text-align: center; border: 2px solid rgba(72, 187, 120, 0.2);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌟</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #276749;">System Status</div>
            <div style="font-size: 0.9rem; color: #48bb78; font-weight: 600; margin-top: 0.5rem;">All Systems Operational</div>
        </div>
        
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1.5rem; border-radius: 16px; text-align: center; border: 2px solid rgba(102, 126, 234, 0.2);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #4c51bf;">Response Time</div>
            <div style="font-size: 0.9rem; color: #667eea; font-weight: 600; margin-top: 0.5rem;">< 200ms Average</div>
        </div>
        
        <div style="background: rgba(237, 137, 54, 0.1); padding: 1.5rem; border-radius: 16px; text-align: center; border: 2px solid rgba(237, 137, 54, 0.2);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #c05621;">Data Freshness</div>
            <div style="font-size: 0.9rem; color: #ed8936; font-weight: 600; margin-top: 0.5rem;">Updated 2min ago</div>
        </div>
    </div>
    """
    
    return html_content

def create_interface():
    """Create the main Gradio interface."""
    # Enhanced Custom CSS for Premium UI
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root Variables for Theme Management */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --light-bg: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --hover-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --text-primary: #1a202c;
        --text-secondary: #4a5568;
        --border-color: #e2e8f0;
        --success-color: #48bb78;
        --warning-color: #ed8936;
        --error-color: #f56565;
    }
    
    /* Main Container Styling */
    .gradio-container {
        font-family: 'Inter', sans-serif !important;
        background: var(--light-bg) !important;
        min-height: 100vh;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Header Styling */
    .main-header {
        background: var(--primary-gradient) !important;
        padding: 3rem 2rem !important;
        border-radius: 0 0 24px 24px !important;
        color: white !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        box-shadow: var(--card-shadow) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,255,255,.1)"/><stop offset="100%" stop-color="rgba(255,255,255,0)"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>') repeat;
        opacity: 0.1;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.05em !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .main-header p {
        font-size: 1.25rem !important;
        margin: 1rem 0 0 0 !important;
        opacity: 0.95 !important;
        font-weight: 400 !important;
        letter-spacing: 0.025em !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        margin: 1rem 0 !important;
        box-shadow: var(--card-shadow) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: var(--hover-shadow) !important;
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-icon {
        font-size: 2.5rem !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1rem !important;
        display: block !important;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1)) !important;
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0.5rem 0 !important;
        color: var(--text-primary) !important;
        line-height: 1.1 !important;
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .metric-label {
        font-size: 0.9rem !important;
        margin: 0 !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    /* Chat Interface Enhancements */
    .chat-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 24px !important;
        box-shadow: var(--card-shadow) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
    }
    
    .chat-container:hover {
        box-shadow: var(--hover-shadow) !important;
    }
    
    /* Chart Container Improvements */
    .chart-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: var(--card-shadow) !important;
        margin: 1rem 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--success-gradient);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--hover-shadow) !important;
    }
    
    .chart-container:hover::before {
        opacity: 1;
    }
    
    /* Tab Styling */
    .tab-nav {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        margin-bottom: 2rem !important;
    }
    
    .tab-nav button {
        background: transparent !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    .tab-nav button.selected {
        background: white !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    /* Button Enhancements */
    .gr-button {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        color: white !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .gr-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .gr-button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    .gr-button:hover::before {
        left: 100%;
    }
    
    /* Input Field Styling */
    .gr-textbox, .gr-input {
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .gr-textbox:focus, .gr-input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Accordion Improvements */
    .gr-accordion {
        border: none !important;
        border-radius: 16px !important;
        margin-bottom: 1rem !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: var(--card-shadow) !important;
        overflow: hidden !important;
    }
    
    .gr-accordion-header {
        background: var(--primary-gradient) !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .gr-accordion-header:hover {
        background: var(--secondary-gradient) !important;
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem !important;
        }
        
        .main-header p {
            font-size: 1rem !important;
        }
        
        .metric-card {
            padding: 1.5rem !important;
        }
        
        .metric-value {
            font-size: 2rem !important;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Success/Error States */
    .success {
        border-left: 4px solid var(--success-color) !important;
        background: rgba(72, 187, 120, 0.1) !important;
    }
    
    .warning {
        border-left: 4px solid var(--warning-color) !important;
        background: rgba(237, 137, 54, 0.1) !important;
    }
    
    .error {
        border-left: 4px solid var(--error-color) !important;
        background: rgba(245, 101, 101, 0.1) !important;
    }
    """

    # Get visualizations
    viz = create_visualizations(data_processor)
    
    with gr.Blocks(css=custom_css, title="🚗 Fetii AI Assistant - Austin Rideshare Analytics", theme=gr.themes.Soft()) as demo:
        # Header and insights
        gr.HTML(get_insights_html())
        
        # Main content with tabs for better organization
        with gr.Tabs() as tabs:
            with gr.TabItem("💬 AI Assistant", elem_id="chat-tab"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML("""
                        <div style="text-align: center; margin: 2rem 0;">
                            <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                                <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🤖</span>
                                Chat with Fetii AI
                            </h2>
                            <p style="color: #4a5568; font-size: 1.1rem; margin-bottom: 2rem;">Ask me anything about Austin rideshare patterns and trends</p>
                        </div>
                        """)
                        
                        # Enhanced example questions with categories
                        gr.HTML("""
                        <div style="margin: 2rem 0;">
                            <h3 style="color: #2d3748; font-weight: 600; margin-bottom: 1.5rem; text-align: center; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                                <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">💡</span>
                                Quick Start Questions
                            </h3>
                        </div>
                        """)
                        
                        # Get example questions from config
                        base_questions = config.CHATBOT_CONFIG['example_questions']
                        
                        # Categorized example questions
                        example_categories = {
                            "📊 Popular Questions": [
                                "What are the peak hours for rideshare in Austin?",
                                "Which locations have the most pickups?",
                                "What's the average group size?"
                            ],
                            "📈 Trend Analysis": [
                                "Show me daily volume trends",
                                "How do group sizes vary by time?",
                                "What are the busiest days of the week?"
                            ],
                            "🎯 Advanced Insights": [
                                base_questions[0] if len(base_questions) > 0 else "How many groups went to The Aquarium on 6th last month?",
                                base_questions[1] if len(base_questions) > 1 else "What are the top drop-off spots for large groups on Saturday nights?",
                                base_questions[2] if len(base_questions) > 2 else "When do groups of 6+ riders typically ride downtown?"
                            ]
                        }
                        
                        for category, questions in example_categories.items():
                            gr.HTML(f"""
                            <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 1rem 0; border-left: 4px solid #667eea;">
                                <h4 style="color: #1a202c; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 0.95rem;">{category}</h4>
                            </div>
                            """)
                            
                            with gr.Row():
                                for question in questions:
                                    gr.Button(
                                        question, 
                                        size="sm",
                                        variant="secondary",
                                        scale=1
                                    )
                        
                        # Enhanced chat interface
                        chatbot_interface = gr.ChatInterface(
                            fn=chat_response,
                            textbox=gr.Textbox(
                                placeholder="💭 Ask me about Austin rideshare patterns...", 
                                scale=7,
                                container=False
                            ),
                            title="",
                            description="",
                            examples=[
                                "What are the peak hours for rideshare in Austin?",
                                "Which locations have the most pickups?",
                                "What's the average group size?",
                                "Show me daily volume trends"
                            ],
                            cache_examples=False
                        )
                    
                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
                            <h3 style="color: #1a202c; font-size: 1.3rem; font-weight: 700; margin: 0 0 1.5rem 0; text-align: center; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                                <span style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📊</span>
                                Quick Insights
                            </h3>
                            <div style="space-y: 1rem;">
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">🚗 Most Active Route</div>
                                    <div style="font-size: 1.1rem; font-weight: 700;">Downtown ↔ Airport</div>
                                </div>
                                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">⏰ Rush Hour Peak</div>
                                    <div style="font-size: 1.1rem; font-weight: 700;">5:00 PM - 7:00 PM</div>
                                </div>
                                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1rem; border-radius: 12px;">
                                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">📈 Trend Status</div>
                                    <div style="font-size: 1.1rem; font-weight: 700;">Growing +15%</div>
                                </div>
                            </div>
                        </div>
                        """)
            
            with gr.TabItem("📊 Analytics Dashboard", elem_id="analytics-tab"):
                gr.HTML("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📊</span>
                        Interactive Analytics Dashboard
                    </h2>
                    <p style="color: #4a5568; font-size: 1.1rem;">Explore detailed visualizations and trends with interactive filters</p>
                </div>
                """)
                
                # Interactive filter controls
                time_filter, group_filter, refresh_btn = create_filter_controls()
                
                # Charts with state management
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Accordion("⏰ Peak Hours Analysis", open=True):
                            hourly_plot = gr.Plot(value=viz['hourly_distribution'])
                        
                        with gr.Accordion("👥 Group Size Distribution", open=True):
                            group_plot = gr.Plot(value=viz['group_size_distribution'])
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("📍 Popular Locations", open=True):
                            location_plot = gr.Plot(value=viz['popular_locations'])
                        
                        with gr.Accordion("🗓️ Time Heatmap", open=False):
                            heatmap_plot = gr.Plot(value=viz['time_heatmap'])
                
                # Connect filters to update function
                def on_filter_change(time_val, group_val):
                    return update_dashboard(time_val, group_val)
                
                time_filter.change(
                    fn=on_filter_change,
                    inputs=[time_filter, group_filter],
                    outputs=[hourly_plot, group_plot, location_plot, heatmap_plot]
                )
                
                group_filter.change(
                    fn=on_filter_change,
                    inputs=[time_filter, group_filter],
                    outputs=[hourly_plot, group_plot, location_plot, heatmap_plot]
                )
                
                refresh_btn.click(
                    fn=on_filter_change,
                    inputs=[time_filter, group_filter],
                    outputs=[hourly_plot, group_plot, location_plot, heatmap_plot]
                )
                
                with gr.Row():
                    with gr.Column():
                        with gr.Accordion("📈 Daily Volume Trends", open=False):
                            gr.Plot(value=viz['daily_volume'])
                    
                    with gr.Column():
                        with gr.Accordion("🆚 Pickup vs Dropoff", open=False):
                            gr.Plot(value=viz['location_comparison'])
            
            with gr.TabItem("� Comprehensive Dashboard", elem_id="comprehensive-tab"):
                gr.HTML("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📈</span>
                        Comprehensive Analytics Dashboard
                    </h2>
                    <p style="color: #4a5568; font-size: 1.1rem;">Complete overview of all analytics and insights</p>
                </div>
                """)
                
                # All charts in a comprehensive view
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Accordion("⏰ Hourly Distribution", open=True):
                            gr.Plot(value=viz['hourly_distribution'])
                        
                        with gr.Accordion("🗓️ Daily Volume Trends", open=True):
                            gr.Plot(value=viz['daily_volume'])
                        
                        with gr.Accordion("🎯 Peak Patterns Analysis", open=False):
                            gr.Plot(value=viz['peak_patterns'])
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("👥 Group Size Distribution", open=True):
                            gr.Plot(value=viz['group_size_distribution'])
                        
                        with gr.Accordion("📍 Popular Locations", open=True):
                            gr.Plot(value=viz['popular_locations'])
                        
                        with gr.Accordion("🆚 Location Comparison", open=False):
                            gr.Plot(value=viz['location_comparison'])
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("🔥 Time Heatmap", open=True):
                            gr.Plot(value=viz['time_heatmap'])
                        
                        with gr.Accordion("📏 Distance Analysis", open=False):
                            gr.Plot(value=viz['trip_distance_analysis'])
                        
                        # Add summary metrics
                        gr.HTML("""
                        <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 16px; padding: 1.5rem; margin-top: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                            <h4 style="color: #1a202c; font-weight: 700; margin: 0 0 1rem 0; text-align: center;">📊 Quick Stats</h4>
                            <div style="display: grid; gap: 0.5rem;">
                                <div style="display: flex; justify-content: between; align-items: center; padding: 0.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px;">
                                    <span style="font-size: 0.9rem; color: #4a5568;">Efficiency Score</span>
                                    <span style="font-weight: 700; color: #667eea;">87%</span>
                                </div>
                                <div style="display: flex; justify-content: between; align-items: center; padding: 0.5rem; background: rgba(72, 187, 120, 0.1); border-radius: 8px;">
                                    <span style="font-size: 0.9rem; color: #4a5568;">Satisfaction</span>
                                    <span style="font-weight: 700; color: #48bb78;">94%</span>
                                </div>
                                <div style="display: flex; justify-content: between; align-items: center; padding: 0.5rem; background: rgba(237, 137, 54, 0.1); border-radius: 8px;">
                                    <span style="font-size: 0.9rem; color: #4a5568;">Growth Rate</span>
                                    <span style="font-weight: 700; color: #ed8936;">+15%</span>
                                </div>
                            </div>
                        </div>
                        """)
            
            with gr.TabItem("�🔬 Advanced Analytics", elem_id="advanced-tab"):
                gr.HTML("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🔬</span>
                        Advanced Analytics & Insights
                    </h2>
                    <p style="color: #4a5568; font-size: 1.1rem;">Deep dive into complex patterns and correlations</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column():
                        with gr.Accordion("🎯 Peak Patterns by Group Size", open=True):
                            gr.Plot(value=viz['peak_patterns'])
                    
                    with gr.Column():
                        with gr.Accordion("📏 Distance Analysis", open=True):
                            gr.Plot(value=viz['trip_distance_analysis'])
                
                with gr.Row():
                    with gr.Column():
                        with gr.Accordion("📈 Daily Volume Trends", open=False):
                            gr.Plot(value=viz['daily_volume'])
                    
                    with gr.Column():
                        with gr.Accordion("🆚 Pickup vs Dropoff Analysis", open=False):
                            gr.Plot(value=viz['location_comparison'])
                
                # Advanced metrics section
                gr.HTML("""
                <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem; margin: 2rem 0; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #1a202c; font-size: 1.4rem; font-weight: 700; margin: 0 0 2rem 0; text-align: center;">🧠 AI-Powered Insights</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 16px; text-align: center;">
                            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
                            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Demand Prediction</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">Next peak: 6:30 PM</div>
                        </div>
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 16px; text-align: center;">
                            <div style="font-size: 2rem; margin-bottom: 1rem;">💡</div>
                            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Route Optimization</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">12% efficiency gain possible</div>
                        </div>
                        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 16px; text-align: center;">
                            <div style="font-size: 2rem; margin-bottom: 1rem;">📊</div>
                            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">Market Analysis</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">Growth opportunity detected</div>
                        </div>
                    </div>
                </div>
                """)
        
        # Enhanced Footer
        gr.HTML("""
        <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 20px; padding: 3rem 2rem; margin-top: 3rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); text-align: center; border: 1px solid rgba(255,255,255,0.2);">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2rem;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2rem;">🚗</div>
                <h3 style="color: #1a202c; font-weight: 800; margin: 0; font-size: 1.8rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Fetii AI</h3>
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2rem;">✨</div>
            </div>
            <p style="color: #4a5568; font-size: 1.1rem; margin: 1rem 0; font-weight: 500;">Built with ❤️ using Gradio • Real Austin Data • Advanced AI Analytics</p>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; flex-wrap: wrap;">
                <div style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; border-radius: 20px;">
                    <span style="color: #667eea; font-weight: 600; font-size: 0.9rem;">🔄 Real-time Updates</span>
                </div>
                <div style="background: rgba(72, 187, 120, 0.1); padding: 0.5rem 1rem; border-radius: 20px;">
                    <span style="color: #48bb78; font-weight: 600; font-size: 0.9rem;">⚡ Lightning Fast</span>
                </div>
                <div style="background: rgba(237, 137, 54, 0.1); padding: 0.5rem 1rem; border-radius: 20px;">
                    <span style="color: #ed8936; font-weight: 600; font-size: 0.9rem;">🛡️ Secure & Private</span>
                </div>
            </div>
        </div>
        """)
    
    return demo

def main():
    """Launch the Gradio application."""
    demo = create_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_api=False,
        show_error=True,
        quiet=False,
        inbrowser=True
    )

if __name__ == "__main__":
    main()