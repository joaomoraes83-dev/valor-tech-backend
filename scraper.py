import os
from serpapi import GoogleSearch
import json

def atualizar_dados():
    # Pega a chave que você salvou no Render
    api_key = os.environ.get("SERPAPI_KEY")
    
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
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(resultados_finais, f, ensure_ascii=False)