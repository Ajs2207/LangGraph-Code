from typing import TypedDict, List
from langchain_core.messages import HumanMessage
# Import ChatOpenRouter from the dedicated package instead of langchain_openai
from langchain_openrouter import ChatOpenRouter
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# Initialise using the dedicated OpenRouter class
# It automatically picks up the OPENROUTER_API_KEY environment variable.
llm = ChatOpenRouter(model="openai/gpt-4o-mini")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
