import streamlit as st
from datetime import datetime
import time
import re
from agent import run_agent  # Import your ReAct Agent

# --- Page configuration ---
st.set_page_config(
    page_title="ReAct Agent - Intelligent Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for modern chat UI ---
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 15px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    .main-header { text-align: center; padding: 2rem 0 1rem 0; background: rgba(255, 255, 255, 0.1); border-radius: 20px; margin-bottom: 2rem; backdrop-filter: blur(10px); }
    .main-title { font-size: 3rem; font-weight: 700; color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); }
    .tagline { font-size: 1.2rem; color: rgba(255, 255, 255, 0.9); margin-top: 0.5rem; font-style: italic; }
    .stChatInputContainer { border-top: 2px solid rgba(255, 255, 255, 0.2); padding-top: 1rem; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
    .stButton button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; border: none; padding: 0.5rem 2rem; font-weight: 600; transition: all 0.3s ease; }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); }
    .message-time { font-size: 0.75rem; color: #666; font-style: italic; margin-top: 0.5rem; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    .thinking { animation: pulse 1.5s ease-in-out infinite; }
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.5); }
    .tool-badge { display: inline-block; padding: 0.2rem 0.6rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; font-size: 0.75rem; margin-right: 0.5rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🧠 ReAct Agent</h1>
    <p class="tagline">Think. Reason. Act. Your Intelligent Conversational Partner</p>
</div>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = {
        "role": "assistant",
        "content": (
            "👋 Hello! I'm your ReAct Agent. I can help you with:\n\n"
            "🔍 **Web Search** - Find information online\n"
            "🌤️ **Weather Updates** - Get current weather for any location\n"
            "💬 **Intelligent Conversations** - Reason through complex problems\n\n"
            "How can I assist you today?"
        ),
        "time": datetime.now().strftime("%H:%M"),
        "tools_used": []
    }
    st.session_state.messages.append(welcome_msg)

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📊 Chat Statistics")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Conversations", st.session_state.conversation_count)
    
    st.markdown("---")
    st.markdown("### 🛠️ Available Tools")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;'>
    🔍 <b>Web Search</b><br><small>Search information online</small><br><br>
    🌤️ <b>Weather Tool</b><br><small>Get weather updates</small><br><br>
    🧠 <b>Groq LLM</b><br><small>Powered reasoning engine</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Try These")
    
    if st.button("🔍 Search latest AI news", use_container_width=True):
        st.session_state.demo_query = "search latest AI news"
        
    if st.button("🌤️ Weather in New York", use_container_width=True):
        st.session_state.demo_query = "what's the weather in New York"
        
    if st.button("💡 Explain quantum computing", use_container_width=True):
        st.session_state.demo_query = "explain quantum computing"
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("ReAct Agent combines reasoning and acting for intelligent task completion using Groq LLM backend.")

# --- Helper: Convert URLs in text to clickable Markdown links ---
def linkify(text):
    url_pattern = re.compile(r"(https?://[^\s]+)")
    return url_pattern.sub(r'[\1](\1)', text)

# --- Display chat messages ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
            st.markdown(f'<p class="message-time">{msg["time"]}</p>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🧠"):
            if msg.get("tools_used"):
                tools_html = "".join([f'<span class="tool-badge">{tool}</span>' for tool in msg["tools_used"]])
                st.markdown(tools_html, unsafe_allow_html=True)
            
            st.markdown(linkify(msg["content"]), unsafe_allow_html=False)
            st.markdown(f'<p class="message-time">{msg["time"]}</p>', unsafe_allow_html=True)

# --- Handle user input ---
if "demo_query" in st.session_state:
    user_input = st.session_state.demo_query
    del st.session_state.demo_query
else:
    user_input = st.chat_input("💬 Type your message here...", key="chat_input")

if user_input:
    timestamp = datetime.now().strftime("%H:%M")
    user_msg = {"role": "user", "content": user_input, "time": timestamp}
    st.session_state.messages.append(user_msg)
    st.session_state.conversation_count += 1
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
        st.markdown(f'<p class="message-time">{timestamp}</p>', unsafe_allow_html=True)
    
    # --- Real agent processing ---
    with st.chat_message("assistant", avatar="🧠"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown('<p class="thinking">🤔 Agent is reasoning...</p>', unsafe_allow_html=True)
        
        try:
            agent_reply = run_agent(user_input)
            thinking_placeholder.empty()
            
            tools_used = []
            if "weather" in user_input.lower():
                tools_used.append("🌤️ Weather")
            elif "search" in user_input.lower() or "latest" in user_input.lower() or "news" in user_input.lower():
                tools_used.append("🔍 Web Search")
            
            if tools_used:
                tools_html = "".join([f'<span class="tool-badge">{tool}</span>' for tool in tools_used])
                st.markdown(tools_html, unsafe_allow_html=True)
            
            # Render reply with clickable links
            st.markdown(linkify(agent_reply), unsafe_allow_html=False)
            
            agent_timestamp = datetime.now().strftime("%H:%M")
            st.markdown(f'<p class="message-time">{agent_timestamp}</p>', unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": agent_reply,
                "time": agent_timestamp,
                "tools_used": tools_used
            })
            
        except Exception as e:
            thinking_placeholder.empty()
            error_msg = f"⚠️ Error: {str(e)}"
            st.markdown(error_msg)
            st.markdown(f'<p class="message-time">{datetime.now().strftime("%H:%M")}</p>', unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "time": datetime.now().strftime("%H:%M"),
                "tools_used": []
            })

# --- Footer ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.7); padding: 1rem;'>
        <p>Powered by ReAct Framework + Groq LLM | Built with ❤️</p>
    </div>
    """, unsafe_allow_html=True)
