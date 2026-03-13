import json
from memory_manager import (
    load_memory,
    save_memory,
    merge_memories,
    format_memory_for_prompt,
)
from llm import extract_memories, chat_with_memory


def load_conversation(file_path="conversation.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("1. Loading conversation...")
    conversation = load_conversation()

    print("2. Loading existing core memory...")
    old_memory = load_memory()
    old_memory_text = format_memory_for_prompt(old_memory)

    print("3. Extracting new memories from conversation...")
    new_memory = extract_memories(conversation, old_memory_text)

    print("New extracted memories:")
    print(json.dumps(new_memory, ensure_ascii=False, indent=2))

    print("4. Merging memories...")
    merged_memory = merge_memories(old_memory, new_memory)

    print("5. Saving core memory...")
    save_memory(merged_memory)

    memory_text = format_memory_for_prompt(merged_memory)

    print("\\n=== Current Core Memory ===")
    print(memory_text)

    print("\\n6. Testing chat with injected memory...")
    test_user_input = "请根据你记住的信息，给我一个今晚可落地的项目启动建议。"
    answer = chat_with_memory(test_user_input, memory_text)

    print("\\n=== Assistant Response ===")
    print(answer)


if __name__ == "__main__":
    main()