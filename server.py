from flask import Flask, jsonify, send_from_directory
import subprocess
import sys
import os

app = Flask(__name__)

bot_process = None

def install_requirements():
    # Instala os pacotes listados no requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print("Erro ao instalar dependências:", e)

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_process
    if bot_process is None:
        install_requirements()
        bot_process = subprocess.Popen([sys.executable, "bot.py"])
        return jsonify(status="Running")
    return jsonify(status="Already running")

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_process
    if bot_process is not None:
        bot_process.terminate()
        bot_process = None
        return jsonify(status="Stopped")
    return jsonify(status="Already stopped")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
