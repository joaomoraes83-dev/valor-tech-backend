import os
from serpapi import GoogleSearch
import json

# Define o caminho do arquivo na pasta atual para evitar erros de permissão no Render
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data.json')

def atualizar_dados():
    api_key = os.environ.get("SERPAPI_KEY", "8cbc27214351554eaf8a44e1d86144c7cd63869909c90363c8ff371550ff179f")
    produtos = ["iPhone 13 128GB", "PlayStation 5"]
    resultados_finais = []

    # 1. Tenta ler os preços antigos para comparar
    precos_antigos = {}
    if os.path.exists(caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados_velhos = json.load(f)
                for item in dados_velhos:
                    # Remove simbolos de moeda para converter em número
                    p_limpo = item['preco'].replace('$', '').replace(',', '').strip()
                    precos_antigos[item['nome']] = float(p_limpo)
        except:
            pass

    for item in produtos:
        params = {
            "engine": "google_shopping",
            "q": item,
            "api_key": api_key,
            "location": "Brazil"
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "shopping_results" in results:
                primeiro = results["shopping_results"][0]
                nome_prod = primeiro.get("title")
                preco_texto = primeiro.get("price")
                
                # Converte preço atual para número
                preco_atual = float(preco_texto.replace('$', '').replace(',', '').strip())
                
                # 2. Calcula a tendência
                tendencia = "Estável"
                if nome_prod in precos_antigos:
                    v_antigo = precos_antigos[nome_prod]
                    if preco_atual > v_antigo:
                        diff = ((preco_atual - v_antigo) / v_antigo) * 100
                        tendencia = f"+{diff:.1f}%"
                    elif preco_atual < v_antigo:
                        diff = ((v_antigo - preco_atual) / v_antigo) * 100
                        tendencia = f"-{diff:.1f}%"

                info = {
                    "nome": nome_prod,
                    "preco": preco_texto,
                    "tendencia": tendencia
                }
                resultados_finais.append(info)
        except Exception as e:
            print(f"Erro: {e}")

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados_finais, f, ensure_ascii=False)

