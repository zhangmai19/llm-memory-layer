```md
# LLM Memory Layer V1

A simple structured memory CLI prototype for LLM applications.

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