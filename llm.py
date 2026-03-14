import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import EXTRACTION_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def generate_assistant_reply(messages, core_memory):
    system_prompt = f"""
You are a helpful AI assistant.

Here is the current long-term memory about the user:
{json.dumps(core_memory, ensure_ascii=False, indent=2)}

Use this memory only when relevant.
Do not mention memory unnaturally.
Be concise, helpful, and natural.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def extract_memory_operations(conversation, current_memory_text=""):
    conversation_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in conversation]
    )

    user_prompt = f"""
Current core memory:
{current_memory_text}

Conversation:
{conversation_text}

Analyze whether any memory should be added, updated, or deleted.
Return JSON only.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end])
            except json.JSONDecodeError:
                pass

        print("Memory operation extraction JSON parse failed. Raw output:")
        print(content)
        return {"operations": []}