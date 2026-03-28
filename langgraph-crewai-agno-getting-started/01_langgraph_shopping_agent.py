"""
LangGraph — Shopping agent with an explicit graph.

Article: https://www.flaviomilan.dev/posts/2026/03/28/langgraph-crewai-agno-getting-started-with-ai-agents/

Prerequisites:
    pip install langgraph langchain-openai langchain
    export OPENAI_API_KEY="sk-..."
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END


# --- Tools (simulated) ---

@tool
def lookup_price(product: str) -> str:
    """Look up the price of a product in USD. Available products: laptop, monitor, keyboard."""
    catalog = {"laptop": 1200.00, "monitor": 450.00, "keyboard": 85.00}
    price = catalog.get(product.lower())
    if price:
        return f"{product}: US$ {price:.2f}"
    return f"Product '{product}' not found."


@tool
def convert_currency(amount: float, from_cur: str, to_cur: str) -> str:
    """Convert an amount between currencies. Available rates: USD↔BRL."""
    rates = {"USD_BRL": 5.20, "BRL_USD": 0.19}
    key = f"{from_cur}_{to_cur}".upper()
    rate = rates.get(key)
    if rate:
        return f"{amount:.2f} {from_cur} = {amount * rate:.2f} {to_cur}"
    return f"Rate {from_cur} → {to_cur} not available."


@tool
def apply_discount(amount: float, percentage: float) -> str:
    """Apply a percentage discount to an amount."""
    final = amount * (1 - percentage / 100)
    return f"Original: {amount:.2f} → With {percentage}% discount: {final:.2f}"


# --- Model and tools setup ---

tools = [lookup_price, convert_currency, apply_discount]
tools_by_name = {t.name: t for t in tools}

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

step = 0


# --- Graph nodes ---

def call_model(state: MessagesState):
    global step
    step += 1
    messages = [
        SystemMessage(
            content="You are a shopping assistant. Always use the available tools "
            "to look up prices, convert currencies, and calculate discounts."
        )
    ] + state["messages"]
    response = model_with_tools.invoke(messages)

    if response.tool_calls:
        print(f"\n--- Step {step}: model decided to call tools ---")
        if response.content:
            print(f"🤔 Thinking: {response.content}")
        for tc in response.tool_calls:
            args_fmt = ", ".join(f"{k}={v!r}" for k, v in tc["args"].items())
            print(f"🔧 Calling: {tc['name']}({args_fmt})")
    else:
        print(f"\n--- Step {step}: final answer ---")

    return {"messages": [response]}


def run_tools(state: MessagesState):
    results = []
    for call in state["messages"][-1].tool_calls:
        tool_fn = tools_by_name[call["name"]]
        result = tool_fn.invoke(call["args"])
        print(f"📎 Result: {result}")
        results.append(
            ToolMessage(content=str(result), tool_call_id=call["id"])
        )
    return {"messages": results}


def decide_next_step(state: MessagesState):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END


# --- Graph assembly ---

graph = StateGraph(MessagesState)
graph.add_node("model", call_model)
graph.add_node("tools", run_tools)
graph.add_edge(START, "model")
graph.add_conditional_edges("model", decide_next_step, ["tools", END])
graph.add_edge("tools", "model")

agent = graph.compile()


# --- Run ---

if __name__ == "__main__":
    question = "I want to buy a laptop. How much in BRL with a 10% discount?"
    print(f"👤 Question: {question}")

    result = agent.invoke({"messages": [HumanMessage(content=question)]})
    print(f"\n💬 Answer: {result['messages'][-1].content}")
