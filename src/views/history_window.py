import customtkinter as ctk
from src import formatar_moeda, ler_historico

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Histórico de Cotações")
        self.geometry("500x400")
        self.resizable(False, False)

        self.grab_set()

        self.criar_widgets()
        self.carregar_historico()

    def criar_widgets(self):
        self.lbl_titulo = ctk.CTkLabel(self, text="Histórico de Cotações", font=("Arial", 18, "bold"))
        self.lbl_titulo.pack(pady=15)

        self.frame_historico = ctk.CTkScrollableFrame(self, width=440, height=300)
        self.frame_historico.pack(padx=20, pady=10, fill="both", expand=True)

    def carregar_historico(self):
        registros = ler_historico()

        if not registros:
            lbl_sem_historico = ctk.CTkLabel(self.frame_historico, text="Nenhum registro encontrado.", font=("Arial", 14))
            lbl_sem_historico.pack(pady=20)
            return

        for item in reversed(registros):
            texto_card = (
                f"Data: {item['data']}\n"
                f"Par: {item['moeda_origem']} -> {item['moeda_destino']} | "
                f"Cotação: {item['cotacao']}\n"
                f"Mín/Máx (24h): {item['min']}/{item['max']}"
            )

            card = ctk.CTkFrame(self.frame_historico)
            card.pack(fill="x", padx=5, pady=5)

            lbl_card = ctk.CTkLabel(card, text=texto_card, justify="left", anchor="w")
            lbl_card.pack(padx=10, pady=8, fill="x")