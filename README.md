# Painel de Cotação

Aplicação desktop em Python para consultar cotações de moedas em tempo real e converter valores entre elas, com histórico de consultas salvo localmente.

## Funcionalidades

- Consulta de cotações em tempo real via [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas)
- Conversão de valores entre duas moedas (ex: USD → BRL)
- Histórico de cotações consultadas, salvo em `data/historico.json`
- Interface gráfica construída com [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Tecnologias

- Python 3
- [customtkinter](https://pypi.org/project/customtkinter/) — interface gráfica
- [requests](https://pypi.org/project/requests/) — requisições HTTP

## Como executar

1. Clone o repositório:
```bash
   git clone https://github.com/LucasBGcomp/Painel_Cotacao.git
   cd Painel_Cotacao
```

2. Instale as dependências:
```bash
   pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
   python main.py
```

## Estrutura do projeto

```
Painel_Cotacao/
├── main.py                    # Ponto de entrada da aplicação
├── src/
│   ├── api.py                 # Consulta de cotações na AwesomeAPI
│   ├── storage.py             # Leitura e escrita do histórico (JSON)
│   ├── utils.py                # Formatação e validação de dados
│   └── views/
│       ├── main_window.py     # Janela principal (conversão)
│       └── history_window.py  # Janela de histórico
└── data/
    └── historico.json         # Histórico de cotações consultadas
```

## Autor

Lucas Espíndula Borges
