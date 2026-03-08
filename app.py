from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import atualizar_dados
import json
import os

app = Flask(__name__)

# Configura o agendador
scheduler = BackgroundScheduler()
scheduler.add_job(func=atualizar_dados, trigger="cron", hour=3, minute=0)
scheduler.start()

# Executa uma vez ao iniciar o servidor
atualizar_dados()

@app.route('/api/precos', methods=['GET'])
def get_precos():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"erro": "Dados não encontrados"}), 404