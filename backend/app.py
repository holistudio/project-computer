from llm.dumbell import DummyModel
from llm.gpt import GPT2Agent
import json


def chat():
    llm = GPT2Agent(temperature=1.4, top_k=25)
    # llm = DummyModel()

    with open("chat_log.txt", "a") as log_file:
        # messages = "Instructions: Have a fun chat with me!\n\n"
        messages = ""
        log_file.write(f"{messages}")

        while True:
            latest = {
                "user_message": "",
                "given_message": "",
                "ai_message": "",
            }
            user_message = input("\n>> ")
            latest["user_message"] = user_message

            messages += f"\nME: {user_message}\n"
            latest["given_message"] = messages

            # print(f"\n\nDEBUG:\n{"*"*10}\n{messages}{"*"*10}\n")
            response = llm.invoke(messages)
            latest["ai_message"] = response

            messages += f"\nBOT: {response}\n"

            print(f"\nai: {response}")

            with open("latest.json",'w') as f:
                json.dump(latest,f)

            log_file.write(f"me: {user_message}\n\n")
            log_file.write(f"ai: {response}\n\n")

if __name__ == "__main__":
    chat()