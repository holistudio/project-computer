from llm.gpt import GPT2Agent
import json
from datetime import datetime


def chat():
    llm = GPT2Agent(temperature=0.7, top_k=25, max_new_tokens=50)

    messages = [
        {"role": "system", "content": "You are a helpful person. Have a fun chat with the user."}
    ]

    log_path = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    with open(log_path, "a") as log_file:
        while True:
            user_input = input("\n>> ")

            messages.append({"role": "user", "content": user_input})
            response = llm.invoke(messages)
            messages.append({"role": "assistant", "content": response})

            print(f"\nai: {response}")

            # Log each turn as a JSONL record — one JSON object per line
            for entry in [
                {"timestamp": datetime.now().isoformat(), "role": "user",      "content": user_input},
                {"timestamp": datetime.now().isoformat(), "role": "assistant", "content": response},
            ]:
                log_file.write(json.dumps(entry) + "\n")
            log_file.flush()  # ensure records survive a crash


if __name__ == "__main__":
    chat()