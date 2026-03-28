"""
Agno — Minimalist agent with plain Python functions.

Article: https://www.flaviomilan.dev/posts/2026/03/28/langgraph-crewai-agno-getting-started-with-ai-agents/

Prerequisites:
    pip install agno openai
    export OPENAI_API_KEY="sk-..."
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat


# --- Tools (plain Python functions — no decorator needed) ---

def lookup_price(product: str) -> str:
    """Look up the price of a product in USD. Available products: laptop, monitor, keyboard.

    Args:
        product: Product name to look up.
    """
    catalog = {"laptop": 1200.00, "monitor": 450.00, "keyboard": 85.00}
    price = catalog.get(product.lower())
    if price:
        return f"{product}: US$ {price:.2f}"
    return f"Product '{product}' not found."


def convert_currency(amount: float, from_cur: str, to_cur: str) -> str:
    """Convert an amount between currencies. Available rates: USD↔BRL.

    Args:
        amount: Numeric amount to convert.
        from_cur: Source currency (e.g. USD).
        to_cur: Target currency (e.g. BRL).
    """
    rates = {"USD_BRL": 5.20, "BRL_USD": 0.19}
    key = f"{from_cur}_{to_cur}".upper()
    rate = rates.get(key)
    if rate:
        return f"{amount:.2f} {from_cur} = {amount * rate:.2f} {to_cur}"
    return f"Rate {from_cur} → {to_cur} not available."


def apply_discount(amount: float, percentage: float) -> str:
    """Apply a percentage discount to an amount.

    Args:
        amount: Original numeric amount.
        percentage: Discount percentage to apply.
    """
    final = amount * (1 - percentage / 100)
    return f"Original: {amount:.2f} → With {percentage}% discount: {final:.2f}"


# --- Agent ---

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[lookup_price, convert_currency, apply_discount],
    instructions="Be direct. Always use the available tools to look up prices, "
    "convert currencies, and calculate discounts.",
    markdown=True,
    debug_mode=True,
)


# --- Run ---

if __name__ == "__main__":
    agent.print_response(
        "I want to buy a laptop. How much in BRL with a 10% discount?",
        stream=True,
        show_full_reasoning=True,
    )
