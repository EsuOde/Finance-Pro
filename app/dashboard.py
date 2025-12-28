import customtkinter as ctk
from database.db import listar_transacoes

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Título Centralizado
        ctk.CTkLabel(self, text="RESUMO FINANCEIRO", font=("Arial", 28, "bold")).pack(pady=40)

        # Container para os Cards
        self.cards_container = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_container.pack(fill="x", padx=50)

        self.atualizar_dados()

    def atualizar_dados(self):
        # 1. Busca os dados do banco usando a sua função listar_transacoes
        dados_receitas = listar_transacoes("receita")
        dados_despesas = listar_transacoes("despesa")

        # 2. Faz a soma (Garante que trata como float para não dar erro de texto)
        total_receitas = sum(float(item[3]) for item in dados_receitas)
        total_despesas = sum(float(item[3]) for item in dados_despesas)
        saldo_final = total_receitas - total_despesas

        # 3. Limpa os cards antigos se houver
        for child in self.cards_container.winfo_children():
            child.destroy()

        # 4. Criar Card de Receitas (Verde)
        card_rec = self.criar_card(self.cards_container, "TOTAL RECEITAS", total_receitas, "#2ecc71")
        card_rec.grid(row=0, column=0, padx=20)

        # 5. Criar Card de Despesas (Vermelho)
        card_des = self.criar_card(self.cards_container, "TOTAL DESPESAS", total_despesas, "#e74c3c")
        card_des.grid(row=0, column=1, padx=20)

        # 6. Card de Saldo Final (Abaixo)
        cor_saldo = "#3498db" if saldo_final >= 0 else "#c0392b"
        self.criar_card(self, "SALDO ATUAL", saldo_final, cor_saldo).pack(pady=30)

    def criar_card(self, parent, titulo, valor, cor):
        frame = ctk.CTkFrame(parent, width=250, height=120, border_width=2, border_color=cor)
        frame.pack_propagate(False)
        
        ctk.CTkLabel(frame, text=titulo, font=("Arial", 14, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(frame, text=f"R$ {valor:,.2f}", font=("Arial", 24, "bold"), text_color=cor).pack()
        
        return frame