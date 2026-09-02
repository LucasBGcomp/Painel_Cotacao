import customtkinter as ctk
from src import *
from src.views.history_window import HistoryWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel de Cotações e Conversão de Moedas")
        self.geometry("540x624")
        self.resizable(False, False)

        self.janela_historico = None

        self.criar_widgets()

    def criar_widgets(self):
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Conversor de Moedas",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_titulo.pack(pady=20)

        self.ent_origem = ctk.CTkEntry(
            self, placeholder_text="Moeda Origem (ex: USD)"
        )
        self.ent_origem.pack(pady=8)

        self.ent_destino = ctk.CTkEntry(
            self, placeholder_text="Moeda Destino (ex: BRL)"
        )
        self.ent_destino.pack(pady=8)

        self.ent_valor = ctk.CTkEntry(
            self, placeholder_text="Valor (ex: 100,00)"
        )
        self.ent_valor.pack(pady=8)

        # Botão de Ação: Convert
        self.btn_converter = ctk.CTkButton(
            self, text="Converter", command=self.executar_conversao
        )
        self.btn_converter.pack(pady=15)

        # Botão para abrir a Janela de Histórico
        self.btn_historico = ctk.CTkButton(
            self,
            text="Ver Histórico de Cotações",
            fg_color="transparent",
            border_width=1,
            command=self.abrir_historico,
        )
        self.btn_historico.pack(pady=5)

        self.lbl_resultado = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=14)
        )
        self.lbl_resultado.pack(pady=20)

    def abrir_historico(self):
        if (self.janela_historico is None or not self.janela_historico.winfo_exists()):
            self.janela_historico = HistoryWindow(self)
        else:
            self.janela_historico.focus()

    def executar_conversao(self):
        try:
            origem = self.ent_origem.get()
            destino = self.ent_destino.get()
            valor = validar_e_converter_valor(self.ent_valor.get())

            self.ent_origem.delete(0, ctk.END)
            self.ent_destino.delete(0, ctk.END)
            self.ent_valor.delete(0, ctk.END)

            dados_cotacao = cotar(origem, destino)
            salvar_historico(dados_cotacao)

            conteudo = list(dados_cotacao.values())[0]
            taxa = (float(conteudo["bid"]) + float(conteudo["ask"])) / 2
            total_convertido = valor * taxa

            resultado_texto = f"Resultado: {formatar_moeda(total_convertido, destino)}\nCotação: {formatar_moeda(taxa, destino)}"
            self.lbl_resultado.configure(
                text=resultado_texto, text_color="green"
            )
        except (ValueError, ConnectionError) as erro:
            self.lbl_resultado.configure(text=str(erro), text_color="red")
        except Exception as erro:
            self.lbl_resultado.configure(
                text=f"Erro inesperado: {erro}", text_color="red"
            )