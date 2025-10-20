import streamlit as st
from datetime import datetime
import re
from agent import run_agent

# Page configuration
st.set_page_config(
    page_title="ReAct Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimalist Custom CSS
st.markdown("""
<style>
    /* Main background */
    .main {
        background: #0f0f0f;
        color: #e0e0e0;
    }
    
    /* Header styling */
    .agent-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .agent-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #00d4ff;
        letter-spacing: 0.1em;
        margin: 0;
    }
    
    .agent-subtitle {
        font-size: 0.9rem;
        color: #888;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #1a1a1a;
        border-left: 3px solid #00d4ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.8rem 0;
    }
    
    [data-testid="stChatMessageContent"] {
        color: #e0e0e0;
    }
    
    /* Tool badges */
    .tool-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        color: #00d4ff;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0 0.25rem 0.5rem 0;
        font-weight: 500;
    }
    
    /* Timestamp */
    .msg-time {
        font-size: 0.7rem;
        color: #555;
        margin-top: 0.5rem;
    }
    
    /* Input area */
    .stChatInputContainer {
        border-top: 1px solid #2a2a2a;
        background: #0f0f0f;
        padding-top: 1rem;
    }
    
    /* Buttons */
    .stButton button {
        background: transparent;
        color: #00d4ff;
        border: 1px solid #00d4ff;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #2a2a2a;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00d4ff;
    }
    
    /* Info box */
    .stAlert {
        background: rgba(0, 212, 255, 0.05);
        border-left: 3px solid #00d4ff;
        color: #e0e0e0;
    }
    
    /* Thinking animation */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .thinking-indicator {
        color: #00d4ff;
        animation: blink 1.5s infinite;
        font-weight: 300;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f0f0f;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a3a;
    }
    
    /* Quick action buttons */
    .quick-action {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        border-color: #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="agent-header">
    <h1 class="agent-title">REACT AGENT</h1>
    <p class="agent-subtitle">Reasoning + Acting Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = {
        "role": "assistant",
        "content": "Hello. I'm your ReAct Agent. I can search the web, check weather, and reason through complex questions. What would you like to know?",
        "time": datetime.now().strftime("%H:%M"),
        "tools": []
    }
    st.session_state.messages.append(welcome)

if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# Sidebar
with st.sidebar:
    st.markdown("### Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Queries", st.session_state.msg_count)
    
    st.markdown("---")
    st.markdown("### Tools")
    st.markdown("🔍 Web Search\n\n🌤️ Weather Data\n\n🧠 LLM Reasoning")
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    if st.button("Latest AI News", use_container_width=True):
        st.session_state.quick_query = "What's the latest news in AI?"
        
    if st.button("Weather NYC", use_container_width=True):
        st.session_state.quick_query = "What's the weather in New York?"
        
    if st.button("Explain Concept", use_container_width=True):
        st.session_state.quick_query = "Explain machine learning simply"
    
    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.rerun()

# Helper function to make URLs clickable
def make_clickable(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.sub(r'[\1](\1)', text)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        if msg.get("tools"):
            tools_html = "".join([f'<span class="tool-indicator">{t}</span>' for t in msg["tools"]])
            st.markdown(tools_html, unsafe_allow_html=True)
        
        st.markdown(make_clickable(msg["content"]))
        st.markdown(f'<div class="msg-time">{msg["time"]}</div>', unsafe_allow_html=True)

# Handle input
user_input = None
if "quick_query" in st.session_state:
    user_input = st.session_state.quick_query
    del st.session_state.quick_query
else:
    user_input = st.chat_input("Ask me anything...")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": timestamp,
        "tools": []
    })
    st.session_state.msg_count += 1
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
        st.markdown(f'<div class="msg-time">{timestamp}</div>', unsafe_allow_html=True)
    
    # Process with agent
    with st.chat_message("assistant", avatar="🤖"):
        status = st.empty()
        status.markdown('<p class="thinking-indicator">● Processing...</p>', unsafe_allow_html=True)
        
        try:
            response = run_agent(user_input)
            status.empty()
            
            # Detect tools used
            tools = []
            query_lower = user_input.lower()
            if any(word in query_lower for word in ["weather", "temperature", "forecast"]):
                tools.append("Weather")
            if any(word in query_lower for word in ["search", "find", "latest", "news"]):
                tools.append("Search")
            
            if tools:
                tools_html = "".join([f'<span class="tool-indicator">{t}</span>' for t in tools])
                st.markdown(tools_html, unsafe_allow_html=True)
            
            st.markdown(make_clickable(response))
            
            reply_time = datetime.now().strftime("%H:%M")
            st.markdown(f'<div class="msg-time">{reply_time}</div>', unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "time": reply_time,
                "tools": tools
            })
            
        except Exception as e:
            status.empty()
            error_msg = f"Error: {str(e)}"
            st.markdown(f"⚠️ {error_msg}")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "time": datetime.now().strftime("%H:%M"),
                "tools": []
            })

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #555; padding: 1rem; font-size: 0.8rem;'>
    ReAct Framework • Groq LLM • Built with Streamlit
</div>
""", unsafe_allow_html=True)
