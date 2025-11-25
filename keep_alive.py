from flask import Flask
from threading import Thread
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return "FunPay Cardinal Bot is running! 🐦", 200

@app.route('/status')
def status():
    return {
        "status": "online",
        "bot": "FunPay Cardinal",
        "version": "0.1.16.9"
    }, 200

@app.route('/ping')
def ping():
    return "pong", 200

def run():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def keep_alive():
    server_thread = Thread(target=run, daemon=True)
    server_thread.start()
    print("[Keep-Alive] HTTP сервер запущен на порту 5000")
