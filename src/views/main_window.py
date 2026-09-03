import customtkinter as ctk
from src import *
from src.views.history_window import HistoryWindow

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel de Cotações e Conversão de Moedas")
        LARGURA = 480
        ALTURA = 620
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
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.lbl_titulo.pack(pady=(25, 5))

        self.lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Consulte cotações em tempo real e converta valores",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
        )
        self.lbl_subtitulo.pack(pady=(0, 20))

        self.card_inputs = ctk.CTkFrame(self, corner_radius=12)
        self.card_inputs.pack(padx=30, pady=10, fill="x")

        # Campo: Moeda Origem
        self.ent_origem = ctk.CTkEntry(
            self.card_inputs,
            placeholder_text="Moeda Origem (ex: USD)",
            width=320,
            height=40,
            corner_radius=8,
        )
        self.ent_origem.pack(pady=(15, 8), padx=20)

        # Campo: Moeda Destino
        self.ent_destino = ctk.CTkEntry(
            self.card_inputs,
            placeholder_text="Moeda Destino (ex: BRL)",
            width=320,
            height=40,
            corner_radius=8,
        )
        self.ent_destino.pack(pady=8, padx=20)

        # Campo: Valor
        self.ent_valor = ctk.CTkEntry(
            self.card_inputs,
            placeholder_text="Valor (ex: 100,00)",
            width=320,
            height=40,
            corner_radius=8,
        )
        self.ent_valor.pack(pady=(8, 15), padx=20)

        # Botão: Converter
        self.btn_converter = ctk.CTkButton(
            self,
            text="Converter",
            width=320,
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.executar_conversao,
        )
        self.btn_converter.pack(pady=20)

        # Container do Resultado
        self.card_resultado = ctk.CTkFrame(self, fg_color="transparent")
        self.card_resultado.pack(padx=30, pady=10, fill="both", expand=True)

        self.lbl_resultado = ctk.CTkLabel(
            self.card_resultado,
            text="",
            font=ctk.CTkFont(size=15, weight="bold"),
            justify="center",
        )
        self.lbl_resultado.pack(expand=True)

        # Botão: Histórico de Cotações
        self.btn_historico = ctk.CTkButton(
            self,
            text="Histórico de Cotações",
            width=220,
            height=32,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            font=ctk.CTkFont(size=13),
            text_color=("gray10", "gray90"),
            command=self.abrir_historico,
        )
        self.btn_historico.pack(pady=(0, 20), side="bottom")

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
        finally:
            self.ent_origem.delete(0, ctk.END)
            self.ent_destino.delete(0, ctk.END)
            self.ent_valor.delete(0, ctk.END)