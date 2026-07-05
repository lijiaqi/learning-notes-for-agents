# ReAct Agent Demo

Minimal ReAct (Reasoning + Acting) agent using OpenAI and Tavily web search.

## Setup

```bash
# Install dependencies
uv sync

# Set API keys in .env
cp .env.example .env
# Add your OPENAI_API_KEY and TAVILY_API_KEY
```

## Run

```bash
uv run python main.py
```

## How it works

The agent follows the ReAct pattern:
1. Receives a question
2. Reasons about what information it needs
3. Calls the `web_search` tool via Tavily
4. Reviews results and either searches again or gives a final answer

The loop runs for up to 5 steps before stopping.
