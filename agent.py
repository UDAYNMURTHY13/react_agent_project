import re
from datetime import datetime
import streamlit as st  # <-- use Streamlit secrets
from langchain_groq import ChatGroq
from tools import web_search_tool, weather_tool
from prompts import REACT_PROMPT, FOLLOW_UP_PROMPT
from typing import Optional

# ---------------- Environment & LLM ---------------- #

# Load API keys from Streamlit secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in Streamlit secrets")
if not OPENWEATHER_API_KEY:
    raise ValueError("Missing OPENWEATHER_API_KEY in Streamlit secrets")
if not TAVILY_API_KEY:
    raise ValueError("Missing TAVILY_API_KEY in Streamlit secrets")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY
)

# ---------------- Helper Functions ---------------- #

def extract_city(query: str) -> Optional[str]:
    """Extract city name from user query."""
    query_lower = query.lower()
    match = re.search(r'(?:weather|temperature) in ([a-zA-Z\s]+)', query_lower)
    if not match:
        match = re.search(r'([a-zA-Z\s]+) (?:weather|temperature)', query_lower)
    if match:
        return match.group(1).strip().title()
    return None

def is_web_searchable(query: str) -> bool:
    """Determine if the query should go to web search."""
    keywords = [
        "latest", "news", "search", "update", "updates", "recent",
        "breaking", "headlines", "trending", "current", "today",
        "AI", "artificial intelligence", "machine learning", "ML",
        "technology", "tech", "software", "hardware", "gadget",
        "smartphone", "computer", "internet", "cyber", "digital",
        "politics", "political", "election", "government", "president",
        "minister", "parliament", "congress", "policy", "legislation",
        "economy", "economic", "finance", "financial", "business",
        "markets", "stock", "trading", "investment", "company",
        "startup", "industry", "commercial", "corporate",
        "science", "scientific", "research", "study", "discovery",
        "experiment", "innovation", "breakthrough", "medical",
        "world", "global", "international", "country", "nation",
        "events", "happening", "occurred", "crisis",
        "sports", "game", "match", "tournament", "championship",
        "player", "team", "score", "movie", "film", "music",
        "celebrity", "entertainment",
        "who is", "what is", "when did", "where is", "how to",
        "why did", "which", "find", "lookup", "tell me about",
        "information", "details", "facts", "data", "statistics",
        "report", "article", "source", "reference"
    ]
    return any(kw.lower() in query.lower() for kw in keywords)

# ---------------- Main Agent Function ---------------- #

def run_agent(query: str) -> str:
    """Executes the ReAct loop with tool integration and LLM fallback."""
    query_lower = query.lower().strip()

    # --- Real-time queries ---
    if "time" in query_lower:
        return f"⏰ The current time is **{datetime.now().strftime('%H:%M:%S')}**"
    if "date" in query_lower:
        return f"📅 Today's date is **{datetime.now().strftime('%Y-%m-%d')}** ({datetime.now().strftime('%A')})"
    if "weather" in query_lower or "rain" in query_lower:
        city = extract_city(query)
        if city:
            print(f"🌤️ Fetching weather for: {city}")
            return weather_tool(city, api_key=OPENWEATHER_API_KEY)
        return "🌍 Please specify a valid city for weather information. Example: 'What's the weather in Paris?'"

    if is_web_searchable(query):
        print(f"🔍 Performing web search for: {query}")
        return web_search_tool(query, api_key=TAVILY_API_KEY)

    # --- Fallback to LLM reasoning ---
    print(f"🧠 User Query (LLM fallback): {query}")
    try:
        formatted_prompt = REACT_PROMPT.format(user_query=query)
        response = llm.invoke(formatted_prompt).content.strip()
        print(f"🤖 Agent Thought: {response}")

        # --- Direct Answer ---
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        # --- Tool Invocation ---
        if "Action:" in response and "Action Input:" in response:
            tool_name = response.split("Action:")[1].split("\n")[0].strip()
            tool_input = response.split("Action Input:")[1].strip()
            print(f"🛠️ Using tool: {tool_name} with input: {tool_input}")

            # Dispatch tool
            tool_name_lower = tool_name.lower()
            if "search" in tool_name_lower:
                observation = web_search_tool(tool_input, api_key=TAVILY_API_KEY)
            elif "weather" in tool_name_lower:
                observation = weather_tool(tool_input, api_key=OPENWEATHER_API_KEY)
            else:
                return f"❌ Unknown tool: {tool_name}. Available tools: Web Search, Weather"

            # Use follow-up LLM prompt for final answer
            formatted_followup = FOLLOW_UP_PROMPT.format(
                tool_name=tool_name,
                observation=observation
            )
            final_answer = llm.invoke(formatted_followup).content.strip()
            if "Final Answer:" in final_answer:
                return final_answer.split("Final Answer:")[-1].strip()
            return final_answer

        return "⚠️ Sorry, I couldn't process that query properly."

    except Exception as e:
        print(f"⚠️ Agent error: {str(e)}")
        return "⚠️ An error occurred while processing your request."


# ---------------- CLI Test Loop ---------------- #
if __name__ == "__main__":
    print("🤖 ReAct Agent (Groq + Web + Weather) initialized!")
    print("📍 Supports weather for any city worldwide")
    print("🔍 Supports web search for latest information\n")

    test_queries = [
        "What's the weather in Paris?",
        "Search for latest AI news",
        "What time is it?",
        "Weather in Tokyo"
    ]

    print("Example queries you can try:")
    for q in test_queries:
        print(f"  - {q}")

    print("\n" + "="*50 + "\n")

    while True:
        user_input = input("Ask something (type 'quit' to exit): ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("👋 Goodbye!")
            break
        if user_input:
            print("\n" + "-"*50)
            answer = run_agent(user_input)
            print(f"\n💬 Agent: {answer}")
            print("-"*50 + "\n")
