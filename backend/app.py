import json
from datetime import datetime
from llm.gpt import GPT2Agent

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__,
            template_folder="../frontend",
            static_folder="../frontend")

llm = GPT2Agent(temperature=0.7, top_k=25, max_new_tokens=50)

# log chat in a file
log_path = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

def log_latest(user_input, response):
    with open(log_path, "a") as log_file:
        # Log each turn as a JSONL record — one JSON object per line
        for entry in [
            {"timestamp": datetime.now().isoformat(), "role": "user",      "content": user_input},
            {"timestamp": datetime.now().isoformat(), "role": "assistant", "content": response},
        ]:
            log_file.write(json.dumps(entry) + "\n")
        log_file.flush()  # ensure records survive a crash

@app.route("/",methods=["GET"])
def root():
    return send_from_directory("index.html")

@app.route("/chat",methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("messages"):
        return jsonify({"error": "Missing or empty 'messages'"}), 400

    messages = data.get("messages", [])
    user_input = messages[-1]["content"]

    response = llm.invoke(messages)

    log_latest(user_input, response)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)