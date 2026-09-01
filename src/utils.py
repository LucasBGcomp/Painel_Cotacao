from datetime import datetime

def formatar_data_br(data: str):
    try:
        dt = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y às %H:%M")
    except ValueError:
        return data

def tratar_codigo_moeda(codigo: str):
    return codigo.strip().upper()

def validar_e_converter_valor(valor_str: str):
    valor_limpo = valor_str.strip().replace(",", ".")

    try:
        valor = float(valor_limpo)
        if valor <= 0:
            raise ValueError("O valor para conversão deve ser maior que zero.")
        return valor
    except ValueError:
        raise ValueError("Digite um número válido para conversão.")

def formatar_moeda(valor: float, codigo: str):
    return f"{valor:,.2f} {tratar_codigo_moeda(codigo)}".replace(",", "v").replace(".", ",").replace("v", ".")