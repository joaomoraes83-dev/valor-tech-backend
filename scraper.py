import os
from serpapi import GoogleSearch
import json

# Define o caminho do arquivo na pasta atual para evitar erros de permissão no Render
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'data.json')

def atualizar_dados():
    # Pega a chave diretamente ou do ambiente do Render
    # Substituí o erro do seu código pela forma correta de ler a chave
    api_key = os.environ.get("SERPAPI_KEY", "8cbc27214351554eaf8a44e1d86144c7cd63869909c90363c8ff371550ff179f")
    
    # Produtos que queremos monitorar
    produtos = ["iPhone 13 128GB", "PlayStation 5"]
    resultados_finais = []

    print("Iniciando busca no Google Shopping...")

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
                info = {
                    "nome": primeiro.get("title"),
                    "preco": primeiro.get("price"),
                    "tendencia": "Consulte o site"
                }
                resultados_finais.append(info)
                print(f"Produto encontrado: {item}")
        except Exception as e:
            print(f"Erro ao buscar {item}: {e}")

    # AGORA ESTAS LINHAS ESTÃO DENTRO DA FUNÇÃO (ALINHADAS)
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados_finais, f, ensure_ascii=False)
    
    print("Arquivo data.json atualizado com sucesso!")
