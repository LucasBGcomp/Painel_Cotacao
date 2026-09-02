import customtkinter as ctk
from src import *
from src.views.history_window import HistoryWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel de Cotações e Conversão de Moedas")
        LARGURA = 500
        ALTURA = 580
        self.centralizar_janela(LARGURA, ALTURA)
        self.resizable(False, False)

        self.janela_historico = None

        self.criar_widgets()

    def centralizar_janela(self, largura: int, altura: int):
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        posx = int((largura_tela - largura) / 2)
        posy = int((altura_tela - altura) / 2)
        self.geometry(f"{largura}x{altura}+{posx}+{posy}")

    def criar_widgets(self):
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Conversor de Moedas",
            font=ctk.CTkFont(size=25, weight="bold"),
        )
        self.lbl_titulo.pack(pady=25)

        self.ent_origem = ctk.CTkEntry(
            self, width=170, height=30, placeholder_text="Moeda Origem (ex: USD)"
        )
        self.ent_origem.pack(pady=8)

        self.ent_destino = ctk.CTkEntry(
            self, width=170, height=30, placeholder_text="Moeda Destino (ex: BRL)"
        )
        self.ent_destino.pack(pady=8)

        self.ent_valor = ctk.CTkEntry(
            self, width=170, height=30,placeholder_text="Valor (ex: 100,00)"
        )
        self.ent_valor.pack(pady=20)

        # Botão de Ação: Convert
        self.btn_converter = ctk.CTkButton(
            self, text="Converter", command=self.executar_conversao, font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_converter.pack(pady=20)

        self.lbl_resultado = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=15)
        )
        self.lbl_resultado.pack(pady=51)

        # Botão para abrir a Janela de Histórico
        self.btn_historico = ctk.CTkButton(
            self,
            text="Ver Histórico de Cotações",
            fg_color="transparent",
            border_width=1,
            command=self.abrir_historico,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.btn_historico.pack(pady=51)

        

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