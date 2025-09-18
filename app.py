import streamlit as st
from data_processor import DataProcessor
from chatbot_engine import FetiiChatbot
from visualizations import create_visualizations
import config
import utils

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.main {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main header with animated gradient */
.main-header {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-header h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.main-header p {
    font-size: 1.2rem;
    margin: 1rem 0 0 0;
    opacity: 0.9;
    font-weight: 300;
}

/* Metric cards with glassmorphism effect */
.metric-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
}

.metric-card h3 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #fff, #f0f8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-card p {
    font-size: 0.9rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-weight: 400;
}

.chat-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    min-height: 400px;
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 5px 20px;
    margin: 1rem 0 1rem 20%;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    font-weight: 500;
    position: relative;
    animation: slideInRight 0.3s ease;
}

.user-message::before {
    content: "👤";
    position: absolute;
    top: -10px;
    right: 10px;
    background: white;
    color: #667eea;
    padding: 5px;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.bot-message {
    background: white;
    color: #2c3e50;
    padding: 1.5rem;
    border-radius: 20px 20px 20px 5px;
    margin: 1rem 20% 1rem 0;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #667eea;
    position: relative;
    animation: slideInLeft 0.3s ease;
    line-height: 1.6;
}

.bot-message::before {
    content: "🤖";
    position: absolute;
    top: -10px;
    left: 10px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 5px;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

@keyframes slideInRight {
    from { transform: translateX(50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-50px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.example-question {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 0.8rem 1.2rem;
    border-radius: 25px;
    margin: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: none;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    font-size: 0.9rem;
}

.example-question:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.5);
    background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
}

.css-1d391kg {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

.stTextInput > div > div > input {
    border-radius: 25px;
    border: 2px solid #e1e8ed;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.8rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 10px;
    color: #2c3e50;
    font-weight: 600;
}

.section-header {
    color: #2c3e50;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    text-align: center;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 2px;
}

.stSpinner > div {
    border-color: #667eea !important;
}

.chart-container {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
    margin: 1rem 0;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.footer {
    text-align: center;
    padding: 2rem;
    color: #7f8c8d;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 15px;
    margin-top: 3rem;
    border-top: 3px solid #667eea;
}

@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    
    .user-message, .bot-message {
        margin-left: 5%;
        margin-right: 5%;
    }
    
    .metric-card h3 {
        font-size: 2rem;
    }
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2, #667eea);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.metric-card {
    animation: fadeInUp 0.6s ease forwards;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Fetii AI Assistant</h1>
        <p>Your intelligent companion for Austin rideshare analytics & insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FetiiChatbot(st.session_state.data_processor)
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: white;">
            <h2 style="margin: 0; font-weight: 700;">📊 Austin Overview</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">Real-time insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        insights = st.session_state.data_processor.get_quick_insights()
        
        st.markdown(f"""
        <div class="metric-card" style="animation-delay: 0.1s;">
            <h3>{insights['total_trips']:,}</h3>
            <p>Total Trips Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="animation-delay: 0.2s;">
            <h3>{insights['avg_group_size']:.1f}</h3>
            <p>Average Group Size</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="animation-delay: 0.3s;">
            <h3>{utils.format_time(insights['peak_hour'])}</h3>
            <p>Peak Hour</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="animation-delay: 0.4s;">
            <h3>{insights['large_groups_pct']:.1f}%</h3>
            <p>Large Groups (6+)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="color: white; text-align: center; margin: 2rem 0 1rem 0;">
            <h3 style="margin: 0; font-weight: 600;">🔥 Hottest Spots</h3>
        </div>
        """, unsafe_allow_html=True)
        
        top_locations = list(insights['top_pickups'])[:5]
        for i, (location, count) in enumerate(top_locations, 1):
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px; color: white;">
                <strong>{i}. {location}</strong><br>
                <small style="opacity: 0.8;">{count} trips</small>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">💬 Chat with Fetii AI</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="color: #2c3e50; font-weight: 600; margin-bottom: 1rem;">✨ Try asking:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        example_questions = config.CHATBOT_CONFIG['example_questions']
        
        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(question, key=f"example_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": question})
                    with st.spinner("🧠 Analyzing data..."):
                        response = st.session_state.chatbot.process_query(question)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #7f8c8d;">
                <h3 style="margin: 0; font-weight: 300;">👋 Hello! I'm your Fetii AI Assistant</h3>
                <p style="margin: 1rem 0 0 0; font-size: 1.1rem;">Ask me anything about Austin rideshare patterns!</p>
                <div style="margin: 2rem 0; font-size: 2rem;">🚗✨🤖</div>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                formatted_content = message["content"].replace('\n', '<br>')
                st.markdown(f'<div class="bot-message">{formatted_content}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1rem 0;"></div>', unsafe_allow_html=True)
        
        if prompt := st.chat_input("💭 Ask me about Austin rideshare patterns..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("🧠 Analyzing data..."):
                response = st.session_state.chatbot.process_query(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    with col2:
        st.markdown('<h2 class="section-header">📈 Live Insights</h2>', unsafe_allow_html=True)
        
        viz = create_visualizations(st.session_state.data_processor)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("⏰ Peak Hours")
        st.plotly_chart(viz['hourly_distribution'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("👥 Group Sizes")
        st.plotly_chart(viz['group_size_distribution'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📍 Top Pickups")
        st.plotly_chart(viz['popular_locations'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <h4 style="margin: 0; color: #2c3e50; font-weight: 600;">🚗 Powered by Fetii AI</h4>
        <p style="margin: 0.5rem 0 0 0;">Built with ❤️ using Streamlit • Real Austin Data • Advanced Analytics</p>
        <div style="margin: 1rem 0; font-size: 1.5rem;">✨🤖✨</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()