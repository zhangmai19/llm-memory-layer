# llm-memory-layer

A minimal MVP for persistent memory extraction with LLMs.

## Features

- Load conversation history
- Extract reusable memory with an LLM
- Save memory into `core_memory.json`
- Inject memory into the next prompt

## Setup

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```
```

---