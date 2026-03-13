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


def extract_memories(conversation, current_memory_text=""):
    conversation_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in conversation]
    )

    user_prompt = f"""
Current core memory:
{current_memory_text}

Conversation:
{conversation_text}

Extract reusable memory from the conversation.
Return JSON only.
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(content[start:end])
        raise ValueError(f"Model did not return valid JSON:\\n{content}")


def build_chat_prompt(user_input, memory_text):
    return [
        {
            "role": "system",
            "content": f"You are a helpful assistant.\\n\\nCore memory:\\n{memory_text}"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]


def chat_with_memory(user_input, memory_text):
    messages = build_chat_prompt(user_input, memory_text)

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content