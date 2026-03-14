import json
import os
from memory_manager import (
    load_memory,
    save_memory,
    format_memory_for_prompt,
    apply_memory_operations,
)
from llm import extract_memory_operations, generate_assistant_reply

CONVERSATION_FILE = "conversation.json"
MEMORY_FILE = "core_memory.json"
LAST_OPERATIONS_FILE = "last_operations.json"


def load_json_file(file_path, default):
    if not os.path.exists(file_path):
        return default

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_conversation(file_path=CONVERSATION_FILE):
    return load_json_file(file_path, [])


def save_conversation(conversation, file_path=CONVERSATION_FILE):
    save_json_file(conversation, file_path)


def load_last_operations(file_path=LAST_OPERATIONS_FILE):
    return load_json_file(file_path, {"operations": []})


def save_last_operations(operation_data, file_path=LAST_OPERATIONS_FILE):
    save_json_file(operation_data, file_path)


def get_current_state():
    return {
        "conversation": load_conversation(),
        "core_memory": load_memory(MEMORY_FILE),
        "last_operations": load_last_operations(),
    }


def process_user_message(user_input):
    conversation = load_conversation()
    core_memory = load_memory(MEMORY_FILE)

    user_message = {"role": "user", "content": user_input}
    conversation.append(user_message)

    recent_messages = conversation[-10:]
    assistant_reply = generate_assistant_reply(recent_messages, core_memory)

    assistant_message = {"role": "assistant", "content": assistant_reply}
    conversation.append(assistant_message)

    save_conversation(conversation, CONVERSATION_FILE)

    current_memory_text = format_memory_for_prompt(core_memory)
    operation_data = extract_memory_operations(conversation[-12:], current_memory_text)

    core_memory = apply_memory_operations(core_memory, operation_data)
    save_memory(core_memory, MEMORY_FILE)
    save_last_operations(operation_data, LAST_OPERATIONS_FILE)

    return {
        "reply": assistant_reply,
        "conversation": conversation,
        "core_memory": core_memory,
        "last_operations": operation_data,
    }


def reset_conversation():
    save_conversation([], CONVERSATION_FILE)
    save_last_operations({"operations": []}, LAST_OPERATIONS_FILE)


def clear_memory():
    save_memory({"memories": []}, MEMORY_FILE)
    save_last_operations({"operations": []}, LAST_OPERATIONS_FILE)