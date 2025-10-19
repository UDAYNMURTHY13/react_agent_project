"""
agent.py
---------
ReAct Agent (Reasoning + Acting) implementation using:
- Groq API for LLM reasoning.
- Web Search Tool for latest information.
- OpenWeatherMap API for weather updates.

Author: Uday N
Capstone Project 3 - ReAct Agent with Web Search and Weather Tools
"""

import os
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from tools import web_search_tool, weather_tool
from prompts import REACT_PROMPT, FOLLOW_UP_PROMPT

# Load environment variables
load_dotenv()

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in .env file")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY
)

# LLM chain for initial reasoning
llm_chain = LLMChain(llm=llm, prompt=REACT_PROMPT)

# LLM chain for follow-up after tool usage
followup_chain = LLMChain(llm=llm, prompt=FOLLOW_UP_PROMPT)


# ---------------- Helper Functions ---------------- #

def extract_city(query: str) -> str | None:
    """Extract city name from user query"""
    query_lower = query.lower()
    match_in = re.search(r'weather in ([a-zA-Z\s]+)', query_lower)
    match_end = re.search(r'([a-zA-Z\s]+) weather', query_lower)
    city = None
    if match_in:
        city = match_in.group(1).strip().title()
    elif match_end:
        city = match_end.group(1).strip().title()
    return city


def is_web_searchable(query: str) -> bool:
    """
    Determine if the query should go to web search.
    Basic heuristic: keywords like 'latest', 'news', 'search', 'update', 'AI', 'politics', etc.
    """
    keywords = [
        # News & Updates
        "latest", "news", "search", "update", "updates", "recent",
        "breaking", "headlines", "trending", "current", "today",
        
        # Technology & AI
        "AI", "artificial intelligence", "machine learning", "ML",
        "technology", "tech", "software", "hardware", "gadget",
        "smartphone", "computer", "internet", "cyber", "digital",
        
        # Politics & Government
        "politics", "political", "election", "government", "president",
        "minister", "parliament", "congress", "policy", "legislation",
        
        # Business & Economy
        "economy", "economic", "finance", "financial", "business",
        "markets", "stock", "trading", "investment", "company",
        "startup", "industry", "commercial", "corporate",
        
        # Science & Research
        "science", "scientific", "research", "study", "discovery",
        "experiment", "innovation", "breakthrough", "medical",
        
        # Global & World Events
        "world", "global", "international", "country", "nation",
        "events", "happening", "occurred", "crisis",
        
        # Sports & Entertainment
        "sports", "game", "match", "tournament", "championship",
        "player", "team", "score", "movie", "film", "music",
        "celebrity", "entertainment",
        
        # Question Words (often need search)
        "who is", "what is", "when did", "where is", "how to",
        "why did", "which", "find", "lookup", "tell me about",
        
        # Informational
        "information", "details", "facts", "data", "statistics",
        "report", "article", "source", "reference"
    ]
    return any(kw.lower() in query.lower() for kw in keywords)


# ---------------- Main Agent Function ---------------- #

def run_agent(query: str) -> str:
    query_lower = query.lower().strip()

    # --- Real-time queries ---
    if "time" in query_lower:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in query_lower:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
    elif "weather" in query_lower or "rain" in query_lower:
        city = extract_city(query)
        if city:
            return weather_tool(city)
        else:
            return "Please specify a valid city for weather information."
    elif is_web_searchable(query):
        return web_search_tool(query)

    # --- Fallback to LLM reasoning ---
    print(f"🧠 User Query (LLM fallback): {query}")
    response = llm_chain.run(user_query=query).strip()
    print(f"🤖 Agent Thought: {response}")

    # --- Direct Answer ---
    if response.startswith("Final Answer:"):
        return response.replace("Final Answer:", "").strip()

    # --- Tool Invocation ---
    elif "Action:" in response and "Action Input:" in response:
        try:
            tool_name = response.split("Action:")[1].split("\n")[0].strip()
            tool_input = response.split("Action Input:")[1].strip()
            print(f"🛠 Using tool: {tool_name} with input: {tool_input}")

            if tool_name.lower() == "web search":
                observation = web_search_tool(tool_input)
            elif tool_name.lower() == "weather":
                observation = weather_tool(tool_input)
            else:
                return f"❌ Unknown tool: {tool_name}"

            # Use follow-up LLM prompt for final answer
            final_answer = followup_chain.run(
                tool_name=tool_name,
                observation=observation
            ).strip()
            return final_answer.replace("Final Answer:", "").strip()

        except Exception as e:
            return f"⚠️ Tool execution error: {str(e)}"

    # --- Unknown response format ---
    else:
        return "⚠️ Sorry, I couldn't process that query properly."


# ---------------- CLI Test Loop ---------------- #
if __name__ == "__main__":
    print("🤖 ReAct Agent (Groq + Web + Weather) initialized!")
    while True:
        user_input = input("\nAsk something (type 'quit' to exit): ")
        if user_input.lower() in ["quit", "exit"]:
            break
        answer = run_agent(user_input)
        print(f"\n💬 Agent: {answer}")
