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


def load_conversation(file_path=CONVERSATION_FILE):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_conversation(conversation, file_path=CONVERSATION_FILE):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)


def print_memory(core_memory):
    memories = core_memory.get("memories", [])
    if not memories:
        print("\n[No memory stored yet]\n")
        return

    print("\n=== Core Memory ===")
    for i, item in enumerate(memories, 1):
        print(f"{i}. [{item['type']}] {item['content']}")
    print()


def main():
    conversation = load_conversation()
    core_memory = load_memory(MEMORY_FILE)

    print("LLM Memory CLI (V2)")
    print("Commands:")
    print("- show memory")
    print("- exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "show memory":
            print_memory(core_memory)
            continue

        user_message = {"role": "user", "content": user_input}
        conversation.append(user_message)

        recent_messages = conversation[-10:]
        assistant_reply = generate_assistant_reply(recent_messages, core_memory)

        print(f"Assistant: {assistant_reply}\n")

        assistant_message = {"role": "assistant", "content": assistant_reply}
        conversation.append(assistant_message)

        save_conversation(conversation, CONVERSATION_FILE)

        current_memory_text = format_memory_for_prompt(core_memory)
        operation_data = extract_memory_operations(conversation[-12:], current_memory_text)

        print("Memory operations:")
        print(json.dumps(operation_data, ensure_ascii=False, indent=2))

        core_memory = apply_memory_operations(core_memory, operation_data)
        save_memory(core_memory, MEMORY_FILE)


if __name__ == "__main__":
    main()