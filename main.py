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
