import json
from datetime import datetime
from llm.gpt import GPT2Agent

from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True, port=5000)