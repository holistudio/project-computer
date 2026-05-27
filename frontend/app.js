const messages = [
  { role: 'system', content: 'You are a helpful person. Have a fun chat with the user.' }
];

const submitBtn = document.querySelector(".message-submit");
const inputBox = document.querySelector('.message-input');

submitBtn.addEventListener('click', async () => {
    const userText = inputBox.value.trim();
    if (!userText) return;
    // console.log("User submitted:", userText);
    inputBox.value = "";

    messages.push({role: "user", content: userText});

    const res = await fetch('/chat', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ messages })
    });

    const data = await res.json();
    // console.log("LLM replied:", data.response);
    messages.push({role: "assistant", content: data.response});
});