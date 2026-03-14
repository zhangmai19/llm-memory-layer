import json
from engine import process_user_message, get_current_state


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
    print("LLM Memory CLI (V2.5)")
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
            state = get_current_state()
            print_memory(state["core_memory"])
            continue

        result = process_user_message(user_input)

        print(f"Assistant: {result['reply']}\n")
        print("Memory operations:")
        print(json.dumps(result["last_operations"], ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()