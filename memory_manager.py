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
    old_items = old_memory.get("memories", [])
    new_items = new_memory.get("memories", [])

    existing = {
        (
            item.get("type", "").strip().lower(),
            item.get("content", "").strip()
        )
        for item in old_items
        if item.get("content", "").strip()
    }

    for item in new_items:
        mem_type = item.get("type", "").strip().lower()
        content = item.get("content", "").strip()

        if not content:
            continue

        key = (mem_type, content)
        if key not in existing:
            old_items.append({
                "type": mem_type,
                "content": content
            })
            existing.add(key)

    old_memory["memories"] = old_items
    return old_memory


def format_memory_for_prompt(memory_data):
    memories = memory_data.get("memories", [])
    if not memories:
        return "No core memory yet."

    lines = []
    for idx, item in enumerate(memories, 1):
        lines.append(f"{idx}. [{item['type']}] {item['content']}")
    return "\n".join(lines)