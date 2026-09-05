const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");

const SESSION_KEY = "chatbot_session_id";
let sessionId = localStorage.getItem(SESSION_KEY) || generateId();
localStorage.setItem(SESSION_KEY, sessionId);

function generateId() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

function addMessage(text, role) {
    const div = document.createElement("div");
    div.classList.add("message", role);
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    userInput.value = "";
    addMessage(message, "user");
    sendBtn.disabled = true;

    const typing = addMessage("Typing...", "bot typing");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: sessionId }),
        });
        const data = await res.json();

        if (!res.ok) throw new Error(data.error || "Request failed");

        sessionId = data.session_id;
        localStorage.setItem(SESSION_KEY, sessionId);
        typing.remove();
        addMessage(data.reply, "bot");
    } catch (err) {
        typing.remove();
        addMessage("Something went wrong. Please try again.", "bot");
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

async function clearChat() {
    await fetch("/api/clear", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
    });
    sessionId = generateId();
    localStorage.setItem(SESSION_KEY, sessionId);
    chatWindow.innerHTML = "";
    addMessage("Hi there! 👋 I'm your AI assistant. How can I help you today?", "bot");
}

sendBtn.addEventListener("click", sendMessage);
clearBtn.addEventListener("click", clearChat);
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

userInput.focus();
