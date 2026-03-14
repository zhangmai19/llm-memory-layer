```md
# LLM Memory Layer V2

A simple Python-based long-term memory system for LLM conversations.

This project explores how to build a memory layer on top of an LLM-powered assistant.  
Instead of treating memory as an append-only notebook, V2 introduces **memory operations**:

- `add`
- `update`
- `delete`

This makes the system more maintainable and closer to a real memory management workflow.

## Features

- CLI multi-turn chat
- Conversation persistence
- Structured long-term memory in JSON
- Automatic memory extraction after each turn
- Simple deduplication

## Setup

```bash
pip install openai python-dotenv
```

Create `.env` from `.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Initialize:

- `conversation.json` with `[]`
- `core_memory.json` with:

```json
{
  "memories": []
}
```

## Run

```bash
python app.py
```

## Commands

- `show memory`
- `exit`
```

---