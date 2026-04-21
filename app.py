import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Configure API Key
api_key = "AIzaSyCjGpD_mZIrUk6AdbwI_x_XBQXdOJYsVVY"
if not api_key:
    print("API Key required.")
    exit()

# Initialize GenAI
client = genai.Client(api_key=api_key)
model_id = 'gemini-2.5-flash-lite'
config = types.GenerateContentConfig(
    system_instruction="You are Jarvis, the highly intelligent and witty AI assistant from Iron Man. Address the user as 'Sharun'. Keep your answers brief."
)

jarvis_chat = client.chats.create(model=model_id, config=config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Empty message"})
        
    try:
        response = jarvis_chat.send_message(user_input)
        clean_text = response.text.replace("*", "")
        return jsonify({"response": clean_text})
    except Exception as e:
        error_msg = "My connection to the servers encountered an error."
        return jsonify({"response": error_msg, "error": str(e)})

if __name__ == "__main__":
    app.run(port=5000)
