# LLM Memory Layer V2.5

A simple Python-based long-term memory system for LLM conversations.

This project explores how to build a memory layer on top of an LLM-powered assistant. Instead of treating memory as an append-only notebook, V2 introduces operation-based memory management:

- `add`
- `update`
- `delete`

This makes the system more maintainable and closer to a real long-term memory workflow.

## Features

- CLI-based multi-turn chat
- Local web UI for testing conversations
- Conversation persistence
- Structured long-term memory in JSON
- Automatic memory extraction after each turn
- Operation-based memory updates
- Simple deduplication
- Real-time core memory inspection
- Memory operations panel
- Reset conversation and clear memory controls

## Project Structure

```text
.
├── app.py
├── cli.py
├── engine.py
├── llm.py
├── memory_manager.py
├── prompts.py
├── README.md
├── requirements.txt
├── .env.example
├── core_memory.example.json
├── conversation.example.json
├── last_operations.json
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install openai python-dotenv
```

Create `.env` from `.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Create `conversation.json` from `conversation.example.json` and initialize it with:

```json
[]
```

Create `core_memory.json` from `core_memory.example.json` and initialize it with:

```json
{
  "memories": []
}
```

Create `last_operations.json` and initialize it with:

```json
[]
```

## Run Web UI

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Run CLI

```bash
python cli.py
```

## Commands

CLI commands:

- `show memory`
- `exit`

## Notes

V2 upgrades the memory system from append-only storage to operation-based updates, allowing the assistant to maintain cleaner and more accurate long-term memory over time.

V2.5 adds a lightweight local web interface for easier testing and debugging, including memory inspection, operation tracking, and reset controls.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
````
