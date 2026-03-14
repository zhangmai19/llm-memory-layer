from flask import Flask, render_template, request, jsonify
from engine import (
    get_current_state,
    process_user_message,
    reset_conversation,
    clear_memory,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state", methods=["GET"])
def state():
    return jsonify(get_current_state())


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    result = process_user_message(message)
    return jsonify(result)


@app.route("/reset", methods=["POST"])
def reset():
    reset_conversation()
    return jsonify(get_current_state())


@app.route("/clear-memory", methods=["POST"])
def clear_memory_route():
    clear_memory()
    return jsonify(get_current_state())


if __name__ == "__main__":
    app.run(debug=True)