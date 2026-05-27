import json
import os
from datetime import datetime
from llm.gpt import GPT2Agent

from flask import Flask, request, jsonify, send_from_directory


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "../frontend"),
            static_folder=os.path.join(BASE_DIR, "../frontend"),
            static_url_path="/static")
# print("Static folder absolute path:", os.path.abspath(app.static_folder))
# print("Exists:", os.path.exists(app.static_folder))

llm = GPT2Agent(temperature=0.7, top_k=25, max_new_tokens=50)
STOP_MARKERS = ("User:", "Assistant:", "me:", "ai:")

# log chat in a file
log_path = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

def clean_response(raw: str) -> str:
    earliest = len(raw)
    for marker in STOP_MARKERS:
        idx = raw.find(marker)
        if idx != -1 and idx < earliest:
            earliest = idx
    return raw[:earliest].rstrip()

# def log_latest(user_input, response, clean):
def log_latest(user_input, response):
    with open(log_path, "a") as log_file:
        # Log each turn as a JSONL record — one JSON object per line
        for entry in [
            {"timestamp": datetime.now().isoformat(), "role": "user",      "content": user_input},
            {"timestamp": datetime.now().isoformat(), "role": "assistant", "content": response},
            # {"timestamp": datetime.now().isoformat(), "role": "assistant", "content": clean, "raw": raw_response},
        ]:
            log_file.write(json.dumps(entry) + "\n")
        log_file.flush()  # ensure records survive a crash

@app.route("/",methods=["GET"])
def root():
    return send_from_directory(app.template_folder, "index.html")

@app.route("/chat",methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("messages"):
        return jsonify({"error": "Missing or empty 'messages'"}), 400

    messages = data.get("messages", [])
    user_input = messages[-1]["content"]

    response = llm.invoke(messages)
    # clean = clean_response(response)

    log_latest(user_input, response)
    # log_latest(user_input, response, clean)

    return jsonify({
        "response": response
        # "response": clean
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)