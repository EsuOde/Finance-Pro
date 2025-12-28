import customtkinter as ctk
from database.db import inserir_transacao, listar_transacoes, deletar_transacao

class Despesas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ctk.CTkLabel(self, text="CONTROLE DE DESPESAS", font=("Arial", 24, "bold"), text_color="#FF6347").pack(pady=20)

        self.form = ctk.CTkFrame(self)
        self.form.pack(pady=10, padx=20, fill="x")

        self.desc = ctk.CTkEntry(self.form, placeholder_text="Ex: Aluguel")
        self.desc.grid(row=0, column=0, padx=10, pady=10)

        self.valor = ctk.CTkEntry(self.form, placeholder_text="R$ 0.00")
        self.valor.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(self.form, text="Registrar Gasto", fg_color="#B22222", 
                      command=self.salvar).grid(row=0, column=2, padx=10, pady=10)

        self.lista_frame = ctk.CTkScrollableFrame(self, label_text="Histórico de Gastos")
        self.lista_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    def salvar(self):
        if self.desc.get() and self.valor.get():
            inserir_transacao("despesa", self.desc.get(), float(self.valor.get()))
            self.desc.delete(0, 'end')
            self.valor.delete(0, 'end')
            self.atualizar_lista()

    def atualizar_lista(self):
        for child in self.lista_frame.winfo_children():
            child.destroy()
        dados = listar_transacoes("despesa")
        for item in dados:
            id_db, tipo, desc, valor = item
            row = ctk.CTkFrame(self.lista_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{desc} - R$ {valor:.2f}", width=300, anchor="w").pack(side="left", padx=10)
            ctk.CTkButton(row, text="Apagar", width=60, fg_color="red", command=lambda i=id_db: self.remover(i)).pack(side="right", padx=5)

    def remover(self, id_item):
        deletar_transacao(id_item)
        self.atualizar_lista()