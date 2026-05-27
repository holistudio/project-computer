const messages = [
  { role: 'system', content: 'You are a helpful person. Have a fun chat with the user.' }
];

const messagesHistory = document.querySelector("#messages-history");

const submitBtn = document.querySelector(".message-submit");
const inputBox = document.querySelector(".message-input");


function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = role === "user" ? "human-message" : "ai-message";
    div.textContent = text;
    messagesHistory.appendChild(div);
    messagesHistory.scrollTop = messagesHistory.scrollHeight;
}

submitBtn.addEventListener('click', async () => {
    const userText = inputBox.value.trim();
    if (!userText) return;
    inputBox.value = "";

    messages.push({ role: "user", content: userText });
    appendMessage("user", userText);

    const res = await fetch('/chat', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages })
    });

    const data = await res.json();
    messages.push({ role: "assistant", content: data.response });
    appendMessage("assistant", data.response);
});