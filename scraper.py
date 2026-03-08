import os
from serpapi import GoogleSearch
import json

# Define o caminho do arquivo na pasta atual
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data.json')

def atualizar_dados():
    # Pega a chave que você salvou no Render
    api_key = os.environ.get("8cbc27214351554eaf8a44e1d86144c7cd63869909c90363c8ff371550ff179f")
    
    # Produtos que queremos monitorar
    produtos = ["iPhone 13 128GB", "PlayStation 5"]
    resultados_finais = []

    for item in produtos:
        # Configura a busca no Google Shopping
        params = {
            "engine": "google_shopping",
            "q": item,
            "api_key": api_key,
            "location": "Brazil"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extrai o primeiro resultado (o mais relevante)
        if "shopping_results" in results:
            primeiro = results["shopping_results"][0]
            info = {
                "nome": primeiro.get("title"),
                "preco": primeiro.get("price"),
                "tendencia": "Consulte o site # Podemos evoluir isso depois"
            }
            resultados_finais.append(info)

    # Salva no arquivo JSON que o Flask vai ler
with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados_finais, f, ensure_ascii=False)