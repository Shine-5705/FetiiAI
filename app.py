import gradio as gr
import os
from dotenv import load_dotenv
from data_processor import DataProcessor
from chatbot_engine import EnhancedFetiiChatbot
from visualizations import create_visualizations
import config
import utils

# Load environment variables
load_dotenv()

# Global data processors and chatbot
data_processor = DataProcessor()
chatbot = None

def initialize_chatbot(api_key=None, use_ai=True):
    """Initialize or update the chatbot with new configuration."""
    global chatbot
    
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key
    
    gemini_api_key = api_key or os.getenv('GEMINI_API_KEY')
    
    chatbot = EnhancedFetiiChatbot(
        data_processor,
        use_ai=use_ai and bool(gemini_api_key),
        gemini_api_key=gemini_api_key
    )
    
    return chatbot

def get_ai_status():
    """Get current AI status for display."""
    if chatbot and hasattr(chatbot, 'ai_available') and chatbot.ai_available:
        return "✅ Gemini AI Active"
    else:
        return "⚠️ Pattern-based Mode"

def chat_response(message, history):
    """Handle chat interactions with the Fetii AI chatbot."""
    if not chatbot:
        initialize_chatbot()
    
    try:
        response = chatbot.process_query(message)
        return response
    except Exception as e:
        return f"I encountered an error processing your request. Please try asking about Austin rideshare data patterns, locations, or statistics."

def update_configuration(api_key, use_ai_enabled):
    """Update chatbot configuration and return status."""
    try:
        initialize_chatbot(api_key, use_ai_enabled)
        status = get_ai_status()
        
        if api_key and use_ai_enabled:
            if chatbot.ai_available:
                return f"✅ Configuration updated successfully! {status}", status
            else:
                return f"❌ Failed to connect to Gemini AI. Check your API key. {get_ai_status()}", get_ai_status()
        else:
            return f"⚠️ Using pattern-based responses. {status}", status
            
    except Exception as e:
        return f"❌ Configuration error: {str(e)}", "❌ Configuration Error"

def get_quick_stats():
    """Get formatted quick statistics."""
    insights = data_processor.get_quick_insights()
    
    stats_text = f"""
**Quick Stats:**
- Total Trips: {insights['total_trips']:,}
- Average Group Size: {insights['avg_group_size']:.1f}
- Peak Hour: {utils.format_time(insights['peak_hour'])}
- Large Groups (6+): {insights['large_groups_pct']:.1f}%
"""
    return stats_text

def get_top_locations():
    """Get formatted top locations."""
    insights = data_processor.get_quick_insights()
    top_locations = list(insights['top_pickups'])[:5]
    
    locations_text = "**Top Pickup Locations:**\n"
    for i, (location, count) in enumerate(top_locations, 1):
        locations_text += f"{i}. {location} - {count} trips\n"
    
    return locations_text

def create_main_interface():
    """Create the main Gradio interface."""
    
    # Initialize chatbot on startup
    initialize_chatbot()
    
    with gr.Blocks(title="Fetii AI Assistant - Austin Rideshare Analytics", theme=gr.themes.Soft()) as demo:
        
        # Header
        gr.Markdown("# Fetii AI Assistant")
        gr.Markdown("Your intelligent companion for Austin rideshare analytics & insights")
        
        # Main content with tabs
        with gr.Tabs():
            
            # Chat Tab
            with gr.TabItem("AI Assistant"):
                with gr.Row():
                    with gr.Column(scale=3):
                        # Example questions
                        gr.Markdown("### Quick Start Questions:")
                        
                        with gr.Row():
                            q1_btn = gr.Button("What are the peak hours?", size="sm")
                            q2_btn = gr.Button("Tell me about West Campus", size="sm")
                        
                        with gr.Row():
                            q3_btn = gr.Button("Show busiest locations", size="sm")
                            q4_btn = gr.Button("How many large groups?", size="sm")
                        
                        # Main chat interface
                        chatbot_interface = gr.ChatInterface(
                            fn=chat_response,
                            textbox=gr.Textbox(placeholder="Ask me about Austin rideshare patterns...", scale=7),
                            title="",
                            description="",
                            examples=[
                                "Hello, how are you?",
                                "What are the peak hours?",
                                "Tell me about popular pickup locations",
                                "How do group sizes vary?"
                            ],
                            cache_examples=False,
                            type="messages"
                        )
                        
                        # Button functions
                        q1_btn.click(lambda: "What are the peak hours for rideshare?", outputs=chatbot_interface.textbox)
                        q2_btn.click(lambda: "Tell me about West Campus pickups", outputs=chatbot_interface.textbox)
                        q3_btn.click(lambda: "Show me the busiest locations", outputs=chatbot_interface.textbox)
                        q4_btn.click(lambda: "How many large groups ride?", outputs=chatbot_interface.textbox)
                    
                    with gr.Column(scale=1):
                        # Quick Stats
                        gr.Markdown("### Quick Stats")
                        stats_display = gr.Markdown(get_quick_stats())
                        
                        # Top Locations
                        gr.Markdown("### Top Pickup Spots")
                        locations_display = gr.Markdown(get_top_locations())
            
            # Analytics Dashboard Tab
            with gr.TabItem("Analytics Dashboard"):
                gr.Markdown("## Interactive Analytics Dashboard")
                gr.Markdown("Explore detailed visualizations and trends")
                
                # Get visualizations
                viz = create_visualizations(data_processor)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Peak Hours Analysis")
                        gr.Plot(value=viz['hourly_distribution'])
                        
                        gr.Markdown("### Group Size Distribution")
                        gr.Plot(value=viz['group_size_distribution'])
                    
                    with gr.Column():
                        gr.Markdown("### Popular Locations")
                        gr.Plot(value=viz['popular_locations'])
                        
                        gr.Markdown("### Time Heatmap")
                        gr.Plot(value=viz['time_heatmap'])
            
            # Advanced Analytics Tab
            with gr.TabItem("Advanced Analytics"):
                gr.Markdown("## Advanced Analytics & Insights")
                gr.Markdown("Deep dive into complex patterns")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Daily Volume Trends")
                        gr.Plot(value=viz['daily_volume'])
                        
                        gr.Markdown("### Peak Patterns by Group")
                        gr.Plot(value=viz['peak_patterns'])
                    
                    with gr.Column():
                        gr.Markdown("### Distance Analysis")
                        gr.Plot(value=viz['trip_distance_analysis'])
                        
                        gr.Markdown("### Location Comparison")
                        gr.Plot(value=viz['location_comparison'])
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("**Powered by Fetii AI** • Enhanced with AI • Real Austin Data • Advanced Analytics")
    
    return demo

def main():
    """Launch the Gradio application."""
    demo = create_main_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_api=False,
        inbrowser=True
    )

if __name__ == "__main__":
    main()