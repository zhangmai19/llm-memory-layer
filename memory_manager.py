import json
import os


def load_memory(file_path="core_memory.json"):
    if not os.path.exists(file_path):
        return {"memories": []}

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory_data, file_path="core_memory.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)


def merge_memories(old_memory, new_memory):
    existing = {
        (item["type"].strip().lower(), item["content"].strip())
        for item in old_memory.get("memories", [])
    }

    for item in new_memory.get("memories", []):
        key = (item["type"].strip().lower(), item["content"].strip())
        if key not in existing:
            old_memory["memories"].append(item)
            existing.add(key)

    return old_memory


def format_memory_for_prompt(memory_data):
    memories = memory_data.get("memories", [])
    if not memories:
        return "No core memory yet."

    lines = []
    for idx, item in enumerate(memories, 1):
        lines.append(f"{idx}. [{item['type']}] {item['content']}")
    return "\n".join(lines)