from pathlib import Path
import webbrowser
from flask import Flask, jsonify, request, send_from_directory
from chatbot import generate_response
import time
from mistralai.client import Mistral
from ai_ori import Chatbot

chatbot = Chatbot()

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    # response = generate_response(message)

    responses, executed = chatbot.continue_conversation(message)
    print("UDAH BALIK")
    if executed:
        write_response = ""
        for r in responses:
            write_response += r["message"]
        responses = write_response

    return jsonify({'response': responses})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    PORT = 8000
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Serving chatbot website at {url}")
    webbrowser.open(url)
    app.run(host='127.0.0.1', port=PORT)
