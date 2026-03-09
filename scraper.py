import os
from serpapi import GoogleSearch
import json
from pymongo import MongoClient
from datetime import datetime

# Caminho do arquivo local (cache)
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data.json')

# Configuração do MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['valortech_db']
colecao = db['historico_precos']

def atualizar_dados():
    # Chave da SerpApi
    api_key = os.environ.get("SERPAPI_KEY", "8cbc27214351554eaf8a44e1d86144c7cd63869909c90363c8ff371550ff179f")
    
    produtos = [
        "iPhone 15 128GB", 
        "iPhone 13 128GB", 
        "PlayStation 5 Slim", 
        "Xbox Series S", 
        "Samsung Galaxy S23", 
        "MacBook Air M2", 
        "Apple Watch Series 9", 
        "iPad 9ª Geração", 
        "Kindle 11ª Geração", 
        "JBL Flip 6"
    ]
    resultados_finais = []

    print(f"Iniciando busca: {datetime.now()}")

    for item in produtos:
        params = {
            "engine": "google_shopping",
            "q": item,
            "api_key": api_key,
            "location": "Brazil",
            "gl": "br",
            "hl": "pt-br",
            "google_domain": "google.com.br"
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "shopping_results" in results:
                primeiro = results["shopping_results"][0]
                nome_prod = primeiro.get("title")
                preco_texto = primeiro.get("price") # Ex: R$ 3.500,00
                
                # Limpeza do preço para cálculo (R$ 3.500,00 -> 3500.00)
                preco_limpo = preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip()
                preco_atual = float(preco_limpo)
                
                # Busca preço anterior no MongoDB para calcular tendência
                registro_antigo = colecao.find_one({"nome_busca": item})
                
                tendencia = "Estável"
                if registro_antigo:
                    v_antigo = registro_antigo['ultimo_preco']
                    if preco_atual > v_antigo:
                        diff = ((preco_atual - v_antigo) / v_antigo) * 100
                        tendencia = f"+{diff:.1f}%"
                    elif preco_atual < v_antigo:
                        diff = ((v_antigo - preco_atual) / v_antigo) * 100
                        tendencia = f"-{diff:.1f}%"

                # Salva o preço atual como "antigo" para a próxima rodada
                colecao.update_one(
                    {"nome_busca": item},
                    {"$set": {"ultimo_preco": preco_atual, "data": datetime.now(), "nome_real": nome_prod}},
                    upsert=True
                )

                resultados_finais.append({
                    "nome": nome_prod,
                    "preco": preco_texto,
                    "tendencia": tendencia
                })
        except Exception as e:
            print(f"Erro no produto {item}: {e}")

    # Salva localmente para o Flask ler
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados_finais, f, ensure_ascii=False)
    print("Dados atualizados com sucesso no MongoDB e data.json")



