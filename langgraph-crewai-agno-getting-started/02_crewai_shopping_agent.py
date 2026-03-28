"""
CrewAI — Two agents collaborating (researcher + analyst).

Article: https://www.flaviomilan.dev/posts/2026/03/28/langgraph-crewai-agno-getting-started-with-ai-agents/

Prerequisites:
    pip install crewai crewai-tools
    export OPENAI_API_KEY="sk-..."
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool


# --- Tools (simulated) ---

@tool("PriceLookup")
def lookup_price(product: str) -> str:
    """Look up the price of a product in USD. Available products: laptop, monitor, keyboard."""
    catalog = {"laptop": 1200.00, "monitor": 450.00, "keyboard": 85.00}
    price = catalog.get(product.lower())
    if price:
        return f"{product}: US$ {price:.2f}"
    return f"Product '{product}' not found."


@tool("CurrencyConverter")
def convert_currency(amount: float, from_cur: str, to_cur: str) -> str:
    """Convert an amount between currencies. Available rates: USD↔BRL. Parameters: numeric amount, source currency (e.g. USD), target currency (e.g. BRL)."""
    rates = {"USD_BRL": 5.20, "BRL_USD": 0.19}
    key = f"{from_cur}_{to_cur}".upper()
    rate = rates.get(key)
    if rate:
        return f"{amount:.2f} {from_cur} = {amount * rate:.2f} {to_cur}"
    return f"Rate {from_cur} → {to_cur} not available."


@tool("Discount")
def apply_discount(amount: float, percentage: float) -> str:
    """Apply a percentage discount. Parameters: numeric amount, discount percentage."""
    final = amount * (1 - percentage / 100)
    return f"Original: {amount:.2f} → With {percentage}% discount: {final:.2f}"


# --- Agents ---

researcher = Agent(
    role="Price researcher",
    goal="Find product prices and convert to the requested currency",
    backstory="International market research specialist.",
    tools=[lookup_price, convert_currency],
    verbose=True,
)

analyst = Agent(
    role="Financial analyst",
    goal="Calculate final amounts with discounts and present a clear summary",
    backstory="Detail-oriented analyst who always shows the numbers.",
    tools=[apply_discount],
    verbose=True,
)


# --- Chained tasks ---

research = Task(
    description="Find the laptop price in USD and convert to BRL.",
    expected_output="The laptop price in BRL.",
    agent=researcher,
)

analysis = Task(
    description="Apply a 10% discount to the BRL price and present a summary "
    "with original price, discount, and final amount.",
    expected_output="Summary with original BRL price, discount amount, and final price.",
    agent=analyst,
)


# --- Crew ---

crew = Crew(
    agents=[researcher, analyst],
    tasks=[research, analysis],
    process=Process.sequential,
    verbose=True,
)


# --- Run ---

if __name__ == "__main__":
    result = crew.kickoff()
    print(f"\n💬 Final result:\n{result}")
