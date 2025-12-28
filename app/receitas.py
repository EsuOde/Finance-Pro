import customtkinter as ctk
from database.db import inserir_transacao, listar_transacoes, deletar_transacao

class Receitas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="GESTÃO DE RECEITAS", font=("Arial", 24, "bold")).pack(pady=20)

        # Container do Formulário
        self.form = ctk.CTkFrame(self)
        self.form.pack(pady=10, padx=20, fill="x")

        self.desc = ctk.CTkEntry(self.form, placeholder_text="Descrição (ex: Salário)", width=250)
        self.desc.grid(row=0, column=0, padx=10, pady=10)

        self.valor = ctk.CTkEntry(self.form, placeholder_text="Valor (R$)", width=100)
        self.valor.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(self.form, text="Adicionar", fg_color="green", command=self.salvar).grid(row=0, column=2, padx=10)

        # Lista de Itens (Onde as receitas aparecem)
        self.lista_frame = ctk.CTkScrollableFrame(self, label_text="Minhas Receitas", height=400)
        self.lista_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    def salvar(self):
        desc = self.desc.get()
        val = self.valor.get()
        if desc and val:
            try:
                inserir_transacao("receita", desc, float(val))
                self.desc.delete(0, 'end')
                self.valor.delete(0, 'end')
                self.atualizar_lista()
            except ValueError:
                print("Erro: Digite um número válido no valor")

    def atualizar_lista(self):
        # Limpa a tela antes de listar
        for child in self.lista_frame.winfo_children():
            child.destroy()

        # Chama a função que você confirmou que está certa
        dados = listar_transacoes("receita")
        
        for item in dados:
            id_db, tipo, desc, valor = item
            row = ctk.CTkFrame(self.lista_frame)
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(row, text=f"{desc}", width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"R$ {valor:.2f}", width=100).pack(side="left", padx=10)
            
            # Botão de apagar vinculado ao ID do banco
            ctk.CTkButton(row, text="Excluir", fg_color="red", width=60,
                          command=lambda i=id_db: self.deletar(i)).pack(side="right", padx=10)

    def deletar(self, id_item):
        deletar_transacao(id_item)
        self.atualizar_lista()