import requests
from src.utils import tratar_codigo_moeda

def cotar(moeda_origem: str, moeda_destino: str):
    origem = tratar_codigo_moeda(moeda_origem)
    destino = tratar_codigo_moeda(moeda_destino)

    url = f"https://economia.awesomeapi.com.br/json/last/{origem}-{destino}"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.HTTPError:
        raise ValueError(f"Par de moedas inválido ou não encontrado: '{origem}-{destino}'")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Falha de conexão ao tentar acessar a API: {e}")