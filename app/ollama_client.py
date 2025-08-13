import requests
import json
import os

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.environ.get("MODEL_NAME", "arivya")

chat_history = []

# Load few-shot examples from training.json
def load_training_examples():
    path = os.path.join(os.path.dirname(__file__), "../data/training.json")
    examples = []
    try:
        with open(path, "r") as f:
            data = json.load(f)
            for item in data:
                examples.append({"role": "user", "content": item["prompt"]})
                examples.append({"role": "assistant", "content": item["response"]})
    except Exception as e:
        print(f"Could not load training examples: {e}")
    return examples

# Add examples to history on startup
chat_history.extend(load_training_examples())

def get_ollama_response(prompt: str) -> str:
    chat_history.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL_NAME,
        "messages": chat_history,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        if response.status_code == 200:
            message = response.json().get("message", {}).get("content", "")
            chat_history.append({"role": "assistant", "content": message})
            return message
        else:
            return f"Ollama error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return "⚠️ Ollama service is currently unavailable. Please try again later."
