const chatBox = document.getElementById("chat-box");
const memoryBox = document.getElementById("memory-box");
const operationsBox = document.getElementById("operations-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const resetBtn = document.getElementById("reset-btn");
const clearMemoryBtn = document.getElementById("clear-memory-btn");
const reloadBtn = document.getElementById("reload-btn");

function renderConversation(conversation) {
    chatBox.innerHTML = "";

    conversation.forEach((msg) => {
        const div = document.createElement("div");
        div.className = `message ${msg.role}`;
        div.textContent = `${msg.role === "user" ? "You" : "Assistant"}: ${msg.content}`;
        chatBox.appendChild(div);
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}

function renderState(state) {
    renderConversation(state.conversation || []);
    memoryBox.textContent = JSON.stringify(state.core_memory || { memories: [] }, null, 2);
    operationsBox.textContent = JSON.stringify(state.last_operations || { operations: [] }, null, 2);
}

async function fetchState() {
    const res = await fetch("/state");
    const data = await res.json();
    renderState(data);
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    sendBtn.disabled = true;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Request failed");
            return;
        }

        renderState(data);
        messageInput.value = "";
        messageInput.focus();
    } catch (err) {
        console.error(err);
        alert("Failed to send message.");
    } finally {
        sendBtn.disabled = false;
    }
}

async function resetConversation() {
    const res = await fetch("/reset", { method: "POST" });
    const data = await res.json();
    renderState(data);
}

async function clearMemory() {
    const res = await fetch("/clear-memory", { method: "POST" });
    const data = await res.json();
    renderState(data);
}

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

resetBtn.addEventListener("click", resetConversation);
clearMemoryBtn.addEventListener("click", clearMemory);
reloadBtn.addEventListener("click", fetchState);

fetchState();