"""
prompts.py
-----------
This module defines all the prompt templates used by the ReAct Agent.

It helps maintain clean separation between logic (agent.py) and
prompt design (ReAct reasoning instructions).

Author: Uday N
Project: Capstone Project 3 - ReAct Agent with Web Search & Weather Tools
"""

from langchain.prompts.prompt import PromptTemplate


# 🔹 Main ReAct decision-making prompt
REACT_PROMPT = PromptTemplate.from_template("""
You are an intelligent AI assistant capable of reasoning and using tools.

Your goal is to help the user by either:
1. Answering directly if you already know the answer.
2. Using one of the available tools: [Web Search, Weather].

Respond using **exactly one** of the following formats:

If you can answer directly:
Final Answer: <your answer>

If you need to use a tool:
Action: <tool_name>
Action Input: <input_for_tool>

User Query: {user_query}
""")

# 🔹 Follow-up prompt template after tool execution
FOLLOW_UP_PROMPT = PromptTemplate.from_template("""
You previously used the tool: {tool_name}.
Here is the observation (tool output):
{observation}

Now, based on this information, provide the final answer to the user.

Respond only in this format:
Final Answer: <final_answer_to_user>
""")
