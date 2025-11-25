from flask import Flask
from threading import Thread
import logging
import time
import requests
import os

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

def self_ping():
    """Пингует приложение каждые 3 минуты для предотвращения засыпания"""
    time.sleep(10)
    
    replit_url = os.getenv('REPLIT_URL') or 'http://localhost:5000'
    
    while True:
        try:
            time.sleep(180)
            requests.get(f"{replit_url}/ping", timeout=5)
            print("[Self-Ping] ✓ Приложение пингировано")
        except Exception as e:
            print(f"[Self-Ping] ✗ Ошибка при пинге: {e}")

def keep_alive():
    server_thread = Thread(target=run, daemon=True)
    server_thread.start()
    print("[Keep-Alive] HTTP сервер запущен на порту 5000")
    
    ping_thread = Thread(target=self_ping, daemon=True)
    ping_thread.start()
    print("[Self-Ping] Поток самопинга запущен (каждые 3 минуты)")
