from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import atualizar_dados
import json
import os

app = Flask(__name__)

scheduler = BackgroundScheduler()
# Executa todo dia às 03:00 da manhã (horário que costuma ser mais tranquilo)
scheduler.add_job(func=atualizar_dados, trigger="cron", hour=3, minute=0)
scheduler.start()

# Rota que o seu app B4A vai chamar
@app.route('/api/precos', methods=['GET'])
def get_precos():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"erro": "Dados não encontrados"}), 404

if __name__ == '__main__':
    # Executa a primeira busca ao iniciar
    atualizar_dados()
    app.run(host='0.0.0.0', port=5000)