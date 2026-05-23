class DummyModel(object):
    def __init__(self):
        pass

    def invoke(self, messages):
        # print(f"\n\nDEBUG:\n{"*"*10}\n{messages}{"*"*10}\n")
        response = "huh?"
        return response
    
def chat():
    llm = DummyModel()

    with open("chat_log.txt", "a") as log_file:
        messages = "Instructions: Have a fun chat with me!\n\n"
        log_file.write(f"{messages}")

        while True:
            user_message = input("\n>: ")

            messages += f"me: {user_message}\n\n"
            
            response = llm.invoke(messages)

            messages += f"ai: {response}\n\n"

            print(f"\nai: {response}")

            log_file.write(f"me: {user_message}\n\n")
            log_file.write(f"ai: {response}\n\n")

if __name__ == "__main__":
    chat()