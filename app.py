import streamlit as st
from data_processor import DataProcessor
from chatbot_engine import FetiiChatbot
from visualizations import create_visualizations
import config
import utils

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🚗",
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Import Tailwind CSS */
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">

/* Import HugeIcons */
<link href="https://cdn.jsdelivr.net/npm/@hugeicons/core@0.0.1/dist/all.min.css" rel="stylesheet">

/* Global Styles */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    min-height: 100vh;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main header */
.main-header {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    padding: 2rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
}

.main-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.025em;
}

.main-header p {
    font-size: 1.125rem;
    margin: 1rem 0 0 0;
    opacity: 0.9;
    font-weight: 400;
    letter-spacing: 0.025em;
}

/* Metric cards */
.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.metric-card h3 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    color: #1e293b;
    line-height: 1.2;
}

.metric-card p {
    font-size: 0.875rem;
    margin: 0.5rem 0 0 0;
    color: #64748b;
    font-weight: 500;
    letter-spacing: 0.025em;
}

.metric-card .icon {
    font-size: 1.5rem;
    color: #3b82f6;
    margin-bottom: 0.5rem;
}

.chat-container {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
    min-height: 400px;
}

.user-message {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 18px 18px 4px 18px;
    margin: 1rem 0 1rem 20%;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    font-weight: 500;
    position: relative;
    animation: slideInRight 0.3s ease;
    line-height: 1.5;
}

.user-message::before {
    content: "";
    position: absolute;
    top: -8px;
    right: 12px;
    width: 24px;
    height: 24px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%233b82f6' viewBox='0 0 24 24'%3E%3Cpath d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'/%3E%3C/svg%3E");
    background-size: 16px 16px;
    background-repeat: no-repeat;
    background-position: center;
}

.bot-message {
    background: #f8fafc;
    color: #1e293b;
    padding: 1.5rem;
    border-radius: 18px 18px 18px 4px;
    margin: 1rem 20% 1rem 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    border-left: 4px solid #3b82f6;
    position: relative;
    animation: slideInLeft 0.3s ease;
    line-height: 1.6;
    letter-spacing: 0.01em;
}

.bot-message::before {
    content: "";
    position: absolute;
    top: -8px;
    left: 12px;
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='white' viewBox='0 0 24 24'%3E%3Cpath d='M20,9V7c0-1.1-0.9-2-2-2h-3c0-1.66-1.34-3-3-3S9,3.34,9,5H6C4.9,5,4,5.9,4,7v2c-1.66,0-3,1.34-3,3s1.34,3,3,3v4c0,1.1,0.9,2,2,2h12c1.1,0,2-0.9,2-2v-4c1.66,0,3-1.34,3-3S21.66,9,20,9z'/%3E%3C/svg%3E");
    background-size: 16px 16px;
    background-repeat: no-repeat;
    background-position: center;
}

.bot-message strong,
.bot-message **text** {
    font-weight: 600;
    color: #0f172a;
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
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    color: #334155;
    padding: 0.875rem 1.25rem;
    border-radius: 12px;
    margin: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid #cbd5e1;
    font-weight: 500;
    font-size: 0.875rem;
    line-height: 1.4;
}

.example-question:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border-color: #3b82f6;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    padding: 1rem 1.25rem;
    font-size: 0.975rem;
    transition: all 0.2s ease;
    background: white;
    font-family: 'Inter', sans-serif;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.875rem 2rem;
    font-weight: 600;
    font-size: 0.975rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    font-family: 'Inter', sans-serif;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
}

.section-header {
    color: #1e293b;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 2rem 0 1rem 0;
    text-align: center;
    position: relative;
    letter-spacing: -0.025em;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 2px;
}

.chart-container {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    margin: 1rem 0;
    border: 1px solid #e2e8f0;
}

.hotspot-item {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 0.875rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.2s ease;
}

.hotspot-item:hover {
    background: rgba(255,255,255,0.2);
    transform: translateX(4px);
}

.hotspot-item strong {
    font-weight: 600;
}

.hotspot-item small {
    opacity: 0.8;
    font-size: 0.8rem;
}

.footer {
    text-align: center;
    padding: 2rem;
    color: #64748b;
    background: white;
    border-radius: 12px;
    margin-top: 3rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
}

.sidebar-header {
    text-align: center;
    padding: 1rem;
    color: white;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 12px;
    margin-bottom: 1rem;
}

.sidebar-header h2 {
    margin: 0;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.025em;
}

.sidebar-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.8;
    font-size: 0.875rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: #64748b;
}

.empty-state h3 {
    margin: 0;
    font-weight: 600;
    font-size: 1.25rem;
    color: #334155;
    letter-spacing: -0.025em;
}

.empty-state p {
    margin: 1rem 0 0 0;
    font-size: 1rem;
    line-height: 1.5;
}

.empty-state .icon-group {
    margin: 2rem 0;
    font-size: 2rem;
    opacity: 0.6;
}

@media (max-width: 768px) {
    .main-header h1 {
        font-size: 1.875rem;
    }
    
    .user-message, .bot-message {
        margin-left: 5%;
        margin-right: 5%;
    }
    
    .metric-card h3 {
        font-size: 1.5rem;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

/* Markdown bold text fix */
.bot-message p strong,
.bot-message strong {
    font-weight: 600 !important;
    color: #0f172a !important;
}

.stMarkdown p strong {
    font-weight: 600 !important;
    color: #0f172a !important;
}
</style>

<!-- D3.js for advanced charts -->
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>Fetii AI Assistant</h1>
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
        <div class="sidebar-header">
            <h2>Austin Overview</h2>
            <p>Real-time insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        insights = st.session_state.data_processor.get_quick_insights()
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">📊</div>
            <h3>{insights['total_trips']:,}</h3>
            <p>Total Trips Analyzed</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">👥</div>
            <h3>{insights['avg_group_size']:.1f}</h3>
            <p>Average Group Size</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">⏰</div>
            <h3>{utils.format_time(insights['peak_hour'])}</h3>
            <p>Peak Hour</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">🎉</div>
            <h3>{insights['large_groups_pct']:.1f}%</h3>
            <p>Large Groups (6+)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="color: #1e293b; text-align: center; margin: 2rem 0 1rem 0;">
            <h3 style="margin: 0; font-weight: 600; font-size: 1.125rem;">Hottest Spots</h3>
        </div>
        """, unsafe_allow_html=True)
        
        top_locations = list(insights['top_pickups'])[:5]
        for i, (location, count) in enumerate(top_locations, 1):
            st.markdown(f"""
            <div class="hotspot-item">
                <strong>{i}. {location}</strong><br>
                <small>{count} trips</small>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">Chat with Fetii AI</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="color: #334155; font-weight: 600; margin-bottom: 1rem; font-size: 1.125rem;">Try asking:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        example_questions = config.CHATBOT_CONFIG['example_questions']
        
        cols = st.columns(2)
        for i, question in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(question, key=f"example_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": question})
                    with st.spinner("Analyzing data..."):
                        response = st.session_state.chatbot.process_query(question)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div class="empty-state">
                <h3>Hello! I'm your Fetii AI Assistant</h3>
                <p>Ask me anything about Austin rideshare patterns!</p>
                <div class="icon-group">🚗 ✨ 🤖</div>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                # Convert markdown bold to HTML strong tags
                formatted_content = message["content"]
                # Replace **text** with <strong>text</strong>
                import re
                formatted_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_content)
                formatted_content = formatted_content.replace('\n', '<br>')
                st.markdown(f'<div class="bot-message">{formatted_content}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1rem 0;"></div>', unsafe_allow_html=True)
        
        if prompt := st.chat_input("Ask me about Austin rideshare patterns..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("Analyzing data..."):
                response = st.session_state.chatbot.process_query(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    with col2:
        st.markdown('<h2 class="section-header">Live Insights</h2>', unsafe_allow_html=True)
        
        viz = create_visualizations(st.session_state.data_processor)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Peak Hours")
        st.plotly_chart(viz['hourly_distribution'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Group Sizes")
        st.plotly_chart(viz['group_size_distribution'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Top Pickups")
        st.plotly_chart(viz['popular_locations'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add new D3.js visualization
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Trip Flow Network")
        
        # Create network data
        df = st.session_state.data_processor.df
        flow_data = df.groupby(['pickup_main', 'dropoff_main']).size().reset_index(name='trips')
        flow_data = flow_data.sort_values('trips', ascending=False).head(15)
        
        network_html = f"""
        <div id="network-chart" style="width: 100%; height: 300px;"></div>
        <script>
        const networkData = {flow_data.to_json(orient='records')};
        
        const width = 400;
        const height = 300;
        
        const svg = d3.select("#network-chart")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
            
        const nodes = [];
        const links = [];
        const nodeMap = new Map();
        
        networkData.forEach(d => {{
            if (!nodeMap.has(d.pickup_main)) {{
                nodeMap.set(d.pickup_main, nodes.length);
                nodes.push({{id: d.pickup_main, type: 'pickup'}});
            }}
            if (!nodeMap.has(d.dropoff_main)) {{
                nodeMap.set(d.dropoff_main, nodes.length);
                nodes.push({{id: d.dropoff_main, type: 'dropoff'}});
            }}
            links.push({{
                source: nodeMap.get(d.pickup_main),
                target: nodeMap.get(d.dropoff_main),
                value: d.trips
            }});
        }});
        
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.index).distance(50))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2));
            
        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke", "#3b82f6")
            .attr("stroke-width", d => Math.sqrt(d.value) / 2)
            .attr("opacity", 0.6);
            
        const node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 6)
            .attr("fill", d => d.type === 'pickup' ? "#10b981" : "#f59e0b")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
                
        node.append("title")
            .text(d => d.id);
            
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
                
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        }});
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        </script>
        """
        st.components.v1.html(network_html, height=350)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <h4 style="margin: 0; color: #1e293b; font-weight: 600;">Powered by Fetii AI</h4>
        <p style="margin: 0.5rem 0 0 0;">Built with love using Streamlit • Real Austin Data • Advanced Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()