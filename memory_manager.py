import json
import os


def load_memory(file_path):
    if not os.path.exists(file_path):
        return {"memories": []}

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory_data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)


def format_memory_for_prompt(memory_data):
    memories = memory_data.get("memories", [])

    if not memories:
        return "No memory stored yet."

    lines = []
    for i, item in enumerate(memories, 1):
        mem_type = item.get("type", "").strip()
        content = item.get("content", "").strip()
        lines.append(f"{i}. [{mem_type}] {content}")

    return "\n".join(lines)


def apply_memory_operations(memory_data, operation_data):
    memories = memory_data.get("memories", [])
    operations = operation_data.get("operations", [])

    def normalize(text):
        return text.strip()

    for op in operations:
        action = op.get("action", "").strip().lower()
        mem_type = op.get("type", "").strip().lower()
        content = normalize(op.get("content", ""))
        old_content = normalize(op.get("old_content", ""))

        if action == "add":
            if not content:
                continue

            exists = any(
                m.get("type", "").strip().lower() == mem_type and
                normalize(m.get("content", "")) == content
                for m in memories
            )
            if not exists:
                memories.append({
                    "type": mem_type,
                    "content": content
                })

        elif action == "update":
            if not old_content or not content:
                continue

            updated = False
            for m in memories:
                if (
                    m.get("type", "").strip().lower() == mem_type and
                    normalize(m.get("content", "")) == old_content
                ):
                    m["content"] = content
                    updated = True
                    break

            if not updated:
                exists = any(
                    m.get("type", "").strip().lower() == mem_type and
                    normalize(m.get("content", "")) == content
                    for m in memories
                )
                if not exists:
                    memories.append({
                        "type": mem_type,
                        "content": content
                    })

        elif action == "delete":
            if not content:
                continue

            memories = [
                m for m in memories
                if not (
                    m.get("type", "").strip().lower() == mem_type and
                    normalize(m.get("content", "")) == content
                )
            ]

    memory_data["memories"] = memories
    return memory_data