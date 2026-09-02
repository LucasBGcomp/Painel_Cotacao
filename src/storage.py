import os
import json
from src.utils import formatar_data_br

arquivo = 'data/historico.json'

def criar_arquivo():
    # Cria a pasta 'data' se não existir
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    # Cria o arquivo se não existir
    if not os.path.exists(arquivo):
        with open(arquivo, 'w', encoding='utf-8') as file:
            json.dump([], file)

criar_arquivo()

def salvar_historico(cotacao: dict):
    conteudo = list(cotacao.values())[0]
    dados = {
        "data" : formatar_data_br(conteudo['create_date']),
        "moeda_origem" : conteudo['code'],
        "moeda_destino" : conteudo['codein'],
        "cotacao" : f"{(float(conteudo['bid']) + float(conteudo['ask'])) / 2:.4f}"
    }

    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            historico = json.load(file)
    except json.JSONDecodeError:
        historico = []

    historico.append(dados)
    with open(arquivo, 'w', encoding='utf-8') as file:
        json.dump(historico, file, indent=4)

def ler_historico():
    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            historico = json.load(file)
    except json.JSONDecodeError:
        historico = []

    return historico
