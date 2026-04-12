from pathlib import Path
import webbrowser
from flask import Flask, abort, jsonify, request, send_from_directory
import time
from mistralai.client import Mistral
from ai import Chatbot
from flask.cli import load_dotenv

load_dotenv()

chatbot = Chatbot()

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR/"static"), static_url_path='/static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')

    responses = chatbot.continue_conversation(message)

    return jsonify({'response': responses})

if __name__ == '__main__':
    PORT = 8000
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Serving chatbot website at {url}")
    webbrowser.open(url)
    app.run(host='127.0.0.1', port=PORT)
