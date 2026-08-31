import unittest
from unittest.mock import MagicMock, patch
import requests
import sys
from pathlib import Path
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))
from src.api import cotar

class TestAPI(unittest.TestCase):
    @patch("src.api.requests.get")
    def test_cotar_sucesso(self, mock_get):
        mock_resposta = MagicMock()
        mock_resposta.status_code = 200
        mock_resposta.json.return_value = {
            "USDBRL": {
                "code": "USD",
                "codein": "BRL",
                "high": "5.50",
                "low": "5.40",
                "bid": "5.45",
                "ask": "5.46",
                "create_date": "2026-08-31 14:00:00",
            }
        }
        mock_get.return_value = mock_resposta

        resultado = cotar(" uSd", "brl ")

        self.assertIn("USDBRL", resultado)
        self.assertEqual(resultado["USDBRL"]["code"], "USD")
        self.assertEqual(resultado["USDBRL"]["codein"], "BRL")

    @patch("src.api.requests.get")
    def test_cotar_moeda_invalida(self, mock_get):
        mock_resposta = MagicMock()
        mock_resposta.raise_for_status.side_effect = (requests.exceptions.HTTPError("404 Client Error"))
        mock_get.return_value = mock_resposta

        with self.assertRaises(ValueError):
            cotar("Invalida", "BRL")

    @patch("src.api.requests.get")
    def test_cotar_falha_conexao(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Erro de Conexão")

        with self.assertRaises(ConnectionError):
            cotar("USD", "BRL")

if __name__ == "__main__":
    unittest.main()