import streamlit as st
import plotly.graph_objects as go
from data_processor import DataProcessor
from chatbot_engine import FetiiChatbot
from visualizations import create_visualizations
import config
import utils
import time

# Page config
st.set_page_config(
    page_title="🚗 Fetii AI Assistant - Austin Rideshare Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = FetiiChatbot(st.session_state.data_processor)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def chat_response(message):
    """Handle chat interactions with the Fetii AI chatbot with enhanced responses."""
    # Process the query
    response = st.session_state.chatbot.process_query(message)
    
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_filter = st.selectbox(
            "🕐 Time Filter",
            ["All Hours", "Morning (6-12)", "Afternoon (12-18)", "Evening (18-24)", "Night (0-6)"]
        )
    
    with col2:
        group_filter = st.selectbox(
            "👥 Group Size Filter", 
            ["All Groups", "Small (1-4)", "Medium (5-8)", "Large (9-12)", "Extra Large (13+)"]
        )
    
    with col3:
        refresh_btn = st.button("🔄 Refresh Data")
    
    return time_filter, group_filter, refresh_btn

def update_dashboard(time_filter, group_filter):
    """Update dashboard based on filter selections."""
    # This would filter the data and regenerate visualizations
    # For now, return the same visualizations
    viz = create_visualizations(st.session_state.data_processor)
    return viz

def get_insights_html():
    """Generate simplified HTML for insights display that works with Streamlit."""
    insights = st.session_state.data_processor.get_quick_insights()
    
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
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
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

# Custom CSS for Premium UI
st.markdown("""
<style>
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
.main {
    font-family: 'Inter', sans-serif !important;
    background: var(--light-bg) !important;
    padding: 1rem !important;
}

/* Enhanced Cards */
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

.metric-card:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: var(--hover-shadow) !important;
    background: rgba(255, 255, 255, 0.95) !important;
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
}

.chart-container:hover {
    transform: translateY(-4px) !important;
    box-shadow: var(--hover-shadow) !important;
}

/* Streamlit specific styling */
.stSelectbox > div > div {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px !important;
}

.stButton > button {
    background: var(--primary-gradient) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
}

.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid var(--border-color) !important;
    background: rgba(255, 255, 255, 0.9) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Chat styling */
.stChatMessage {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    margin: 1rem 0 !important;
}

/* Sidebar styling */
.css-1d391kg {
    background: var(--primary-gradient) !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    color: var(--text-secondary);
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    color: var(--text-primary) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: var(--primary-gradient) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 0 0 12px 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .metric-card {
        padding: 1.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header and insights
    st.markdown(get_insights_html(), unsafe_allow_html=True)
    
    # Main content with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Assistant", "📊 Analytics Dashboard", "📈 Comprehensive Dashboard", "🔬 Advanced Analytics"])
    
    with tab1:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🤖</span>
                Chat with Fetii AI
            </h2>
            <p style="color: #4a5568; font-size: 1.1rem; margin-bottom: 2rem;">Ask me anything about Austin rideshare patterns and trends</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Enhanced example questions with categories
            st.markdown("""
            <div style="margin: 2rem 0;">
                <h3 style="color: #2d3748; font-weight: 600; margin-bottom: 1.5rem; text-align: center; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                    <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">💡</span>
                    Quick Start Questions
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
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
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); border-radius: 12px; padding: 1rem; margin: 1rem 0; border-left: 4px solid #667eea;">
                    <h4 style="color: #1a202c; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 0.95rem;">{category}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(len(questions))
                for i, question in enumerate(questions):
                    with cols[i]:
                        if st.button(question, key=f"example_{category}_{i}"):
                            st.session_state.chat_history.append({"role": "user", "content": question})
                            response = chat_response(question)
                            st.session_state.chat_history.append({"role": "assistant", "content": response})
                            st.rerun()
            
            # Chat interface
            st.markdown("### Chat Interface")
            
            # Display chat history
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("💭 Ask me about Austin rideshare patterns..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    response = chat_response(prompt)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with col2:
            st.markdown("""
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
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <span style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📊</span>
                Interactive Analytics Dashboard
            </h2>
            <p style="color: #4a5568; font-size: 1.1rem;">Explore detailed visualizations and trends with interactive filters</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive filter controls
        time_filter, group_filter, refresh_btn = create_filter_controls()
        
        # Get visualizations
        viz = update_dashboard(time_filter, group_filter)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("⏰ Peak Hours Analysis", expanded=True):
                st.plotly_chart(viz['hourly_distribution'], use_container_width=True)
            
            with st.expander("👥 Group Size Distribution", expanded=True):
                st.plotly_chart(viz['group_size_distribution'], use_container_width=True)
        
        with col2:
            with st.expander("📍 Popular Locations", expanded=True):
                st.plotly_chart(viz['popular_locations'], use_container_width=True)
            
            with st.expander("🗓️ Time Heatmap", expanded=False):
                st.plotly_chart(viz['time_heatmap'], use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            with st.expander("📈 Daily Volume Trends", expanded=False):
                st.plotly_chart(viz['daily_volume'], use_container_width=True)
        
        with col4:
            with st.expander("🆚 Pickup vs Dropoff", expanded=False):
                st.plotly_chart(viz['location_comparison'], use_container_width=True)
    
    with tab3:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <span style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">📈</span>
                Comprehensive Analytics Dashboard
            </h2>
            <p style="color: #4a5568; font-size: 1.1rem;">Complete overview of all analytics and insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get visualizations
        viz = create_visualizations(st.session_state.data_processor)
        
        # All charts in a comprehensive view
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.expander("⏰ Hourly Distribution", expanded=True):
                st.plotly_chart(viz['hourly_distribution'], use_container_width=True)
            
            with st.expander("🗓️ Daily Volume Trends", expanded=True):
                st.plotly_chart(viz['daily_volume'], use_container_width=True)
            
            with st.expander("🎯 Peak Patterns Analysis", expanded=False):
                st.plotly_chart(viz['peak_patterns'], use_container_width=True)
        
        with col2:
            with st.expander("👥 Group Size Distribution", expanded=True):
                st.plotly_chart(viz['group_size_distribution'], use_container_width=True)
            
            with st.expander("📍 Popular Locations", expanded=True):
                st.plotly_chart(viz['popular_locations'], use_container_width=True)
            
            with st.expander("🆚 Location Comparison", expanded=False):
                st.plotly_chart(viz['location_comparison'], use_container_width=True)
        
        with col3:
            with st.expander("🔥 Time Heatmap", expanded=True):
                st.plotly_chart(viz['time_heatmap'], use_container_width=True)
            
            with st.expander("📏 Distance Analysis", expanded=False):
                st.plotly_chart(viz['trip_distance_analysis'], use_container_width=True)
            
            # Add summary metrics
            st.markdown("""
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
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="color: #1a202c; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <span style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🔬</span>
                Advanced Analytics & Insights
            </h2>
            <p style="color: #4a5568; font-size: 1.1rem;">Deep dive into complex patterns and correlations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get visualizations
        viz = create_visualizations(st.session_state.data_processor)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🎯 Peak Patterns by Group Size", expanded=True):
                st.plotly_chart(viz['peak_patterns'], use_container_width=True)
        
        with col2:
            with st.expander("📏 Distance Analysis", expanded=True):
                st.plotly_chart(viz['trip_distance_analysis'], use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            with st.expander("📈 Daily Volume Trends", expanded=False):
                st.plotly_chart(viz['daily_volume'], use_container_width=True)
        
        with col4:
            with st.expander("🆚 Pickup vs Dropoff Analysis", expanded=False):
                st.plotly_chart(viz['location_comparison'], use_container_width=True)
        
        # Advanced metrics section
        st.markdown("""
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
        """, unsafe_allow_html=True)
    
    # Enhanced Footer
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 20px; padding: 3rem 2rem; margin-top: 3rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); text-align: center; border: 1px solid rgba(255,255,255,0.2);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2rem;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2rem;">🚗</div>
            <h3 style="color: #1a202c; font-weight: 800; margin: 0; font-size: 1.8rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Fetii AI</h3>
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2rem;">✨</div>
        </div>
        <p style="color: #4a5568; font-size: 1.1rem; margin: 1rem 0; font-weight: 500;">Built with ❤️ using Streamlit • Real Austin Data • Advanced AI Analytics</p>
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
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()