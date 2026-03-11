# Simple GPT Agent Demo (Simulated Weather)

## Overview
This demo is a small, modular Ollama-powered agent. It will call the local Ollama AI model.

## Features
- Reasoning via Ollama
- Tools: summarizer, joke generator, simulated weather
- In-memory conversation history
- CLI interface

## Setup
1. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv simple_agent
   source simple_agent/bin/activate  # macOS / Linux
   .\simple_agent\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
2. Run the demo:
   ```bash
   python main.py
   ```

## Example Prompts
- `Summarize: <text>` → uses summarizer tool
- `Tell me a joke` → uses joke tool
- `What's the weather in London?` → uses simulated weather tool
- `Show me the log` → output all the logs from memory
- Any other question is sent to Ollama (without thinking)

