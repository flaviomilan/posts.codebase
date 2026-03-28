# LangGraph, CrewAI, and Agno — getting started with AI agents

Source code for the blog post:
- 🇺🇸 [LangGraph, CrewAI, and Agno: getting started with AI agents](https://www.flaviomilan.dev/posts/2026/03/28/langgraph-crewai-agno-getting-started-with-ai-agents/)
- 🇧🇷 [LangGraph, CrewAI e Agno: primeiros passos com agentes de IA](https://www.flaviomilan.dev/pt-br/posts/2026/03/28/langgraph-crewai-agno-primeiros-passos-com-agentes-de-ia/)

## What this code does

Three implementations of the **same problem** using different AI agent frameworks:

> "I want to buy a laptop. How much in BRL with a 10% discount?"

The agent needs to:
1. **Look up the price** of the product (US$ 1,200.00)
2. **Convert** from USD to BRL (R$ 6,240.00)
3. **Apply the discount** of 10% (R$ 5,616.00)

Each script uses the same set of tools but orchestrates the agent differently.

## Files

| File | Framework | Description |
|------|-----------|-------------|
| `01_langgraph_shopping_agent.py` | LangGraph | Explicit graph with nodes and edges — maximum control |
| `02_crewai_shopping_agent.py` | CrewAI | Two agents (researcher + analyst) collaborating |
| `03_agno_shopping_agent.py` | Agno | Minimalist agent with plain Python functions |

## Prerequisites

- **Python 3.10, 3.11, or 3.12** (required)
  - ⚠️ Python 3.13+ **does not work** with CrewAI (tiktoken/PyO3 incompatibility)
  - To check: `python3 --version`
- **OpenAI API key** ([how to get one](https://platform.openai.com/api-keys))

## Setup

### 1. Create a virtual environment

```bash
# If you have multiple Python versions, use 3.12 explicitly:
python3.12 -m venv .venv

# Or, if python3 is already 3.10–3.12:
python3 -m venv .venv
```

### 2. Activate the environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

> 💡 Tip: create a `.env` file with `OPENAI_API_KEY=sk-...` so you don't have to export it every time. The `.env` is already in `.gitignore`.

## Running the examples

### LangGraph

```bash
python 01_langgraph_shopping_agent.py
```

Expected output:
```
👤 Question: I want to buy a laptop. How much in BRL with a 10% discount?

--- Step 1: model decided to call tools ---
🔧 Calling: lookup_price(product='laptop')
📎 Result: laptop: US$ 1200.00

--- Step 2: model decided to call tools ---
🔧 Calling: convert_currency(amount=1200.0, from_cur='USD', to_cur='BRL')
📎 Result: 1200.00 USD = 6240.00 BRL

--- Step 3: model decided to call tools ---
🔧 Calling: apply_discount(amount=6240.0, percentage=10.0)
📎 Result: Original: 6240.00 → With 10% discount: 5616.00

--- Step 4: final answer ---

💬 Answer: The laptop costs R$ 5,616.00 with a 10% discount.
```

### CrewAI

```bash
python 02_crewai_shopping_agent.py
```

With `verbose=True`, CrewAI shows each agent's internal reasoning — the researcher looks up and converts, then the analyst applies the discount.

### Agno

```bash
python 03_agno_shopping_agent.py
```

With `debug_mode=True`, Agno shows tool calls and usage metrics.

## Notes

- Scripts use `gpt-4o-mini` by default (cheapest). Switch to `gpt-4o` for more elaborate responses.
- Tools use simulated data (fixed catalog, fixed exchange rate). In production, they'd connect to real APIs.
- Cost per run is approximately US$ 0.001–0.005 (fractions of a cent).
