const submitBtn = document.querySelector(".message-submit");
const inputBox = document.querySelector('.message-input');

submitBtn.addEventListener('click', () => {
    const userText = inputBox.value.trim();
    if (!userText) return;

    // console.log("User submitted:", userText);
    inputBox.value = "";
});