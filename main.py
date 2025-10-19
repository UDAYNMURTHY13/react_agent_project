"""
main.py
--------
Entry point for the ReAct Agent App.

This script runs an interactive command-line chat session
where the user can ask questions, and the Groq-powered ReAct Agent
decides whether to:
1. Answer directly,
2. Use the Web Search tool, or
3. Use the Weather tool.

Author: Uday N
Project: Capstone Project 3 - ReAct Agent with Web Search & Weather Tools
"""

import os
from dotenv import load_dotenv
from agent import run_agent

def main():
    """Main function to run the ReAct Agent interactively."""
    load_dotenv()  # Load API keys and environment variables

    print("=" * 60)
    print("🤖 ReAct Agent - Groq Powered (Web Search + Weather Tools)")
    print("=" * 60)
    print("\nAvailable capabilities:")
    print("🔹 Direct Question Answering")
    print("🔹 Web Search (latest info)")
    print("🔹 Weather Information (via OpenWeather API)")
    print("\nType 'quit' or 'exit' anytime to leave.\n")

    while True:
        try:
            user_query = input("🧠 Enter your query: ").strip()
            if user_query.lower() in ["quit", "exit"]:
                print("\n👋 Goodbye! Have a great day.")
                break

            answer = run_agent(user_query)
            print(f"\n💬 Agent: {answer}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Exiting gracefully.")
            break
        except Exception as e:
            print(f"⚠️ Error: {str(e)}\n")

if __name__ == "__main__":
    main()
