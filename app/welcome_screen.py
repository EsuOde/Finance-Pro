import customtkinter as ctk
from tkinter import messagebox
from database.db import login_usuario, cadastrar_usuario, recuperar_senha
import json
import os

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, login_success_callback):
        super().__init__(parent, fg_color="#f0f2f5") 
        self.login_success_callback = login_success_callback
        self.prefs_file = "prefs.json"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Card Branco
        self.card = ctk.CTkFrame(self, fg_color="white", width=400, height=600, corner_radius=30)
        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)

        # Títulos
        ctk.CTkLabel(self.card, text="FINANCE", font=("Inter", 48, "bold"), text_color="#2c3e50").pack(pady=(60, 0))
        ctk.CTkLabel(self.card, text="SYSTEM PRO", font=("Inter", 14, "bold"), text_color="#7f8c8d").pack(pady=(0, 40))

        # Inputs
        self.entry_user = ctk.CTkEntry(self.card, placeholder_text="👤 Usuário", width=320, height=50, 
                                       fg_color="#f8f9fa", border_color="#dcdde1", text_color="black", corner_radius=15)
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self.card, placeholder_text="🔒 Senha", width=320, height=50, 
                                       fg_color="#f8f9fa", border_color="#dcdde1", text_color="black", corner_radius=15, show="*")
        self.entry_pass.pack(pady=10)

        # Frame de Utilitários
        utils = ctk.CTkFrame(self.card, fg_color="transparent")
        utils.pack(fill="x", padx=45, pady=5)
        
        self.check_remember = ctk.CTkCheckBox(
            utils, text="Lembrar-me", font=("Inter", 12, "bold"), text_color="#2c3e50",
            fg_color="#4a90e2", hover_color="#357abd", border_color="#4a90e2"
        )
        self.check_remember.pack(side="left")
        
        btn_esqueci = ctk.CTkButton(
            utils, text="Esqueci a senha?", font=("Inter", 11, "bold"), text_color="#3498db", 
            fg_color="transparent", hover=True, hover_color="#f1f2f6", width=10, command=self.acao_esqueci_senha
        )
        btn_esqueci.pack(side="right")
        btn_esqueci.bind("<Enter>", lambda e: btn_esqueci.configure(text_color="#2980b9"))
        btn_esqueci.bind("<Leave>", lambda e: btn_esqueci.configure(text_color="#3498db"))

        # Botão ENTRAR
        self.btn_login = ctk.CTkButton(self.card, text="ENTRAR", width=320, height=55, font=("Inter", 16, "bold"), 
                                       fg_color="#4a90e2", hover_color="#357abd", corner_radius=15, command=self.executar_login)
        self.btn_login.pack(pady=(40, 10))

        # Botão CRIAR NOVA CONTA
        self.btn_cadastrar = ctk.CTkButton(self.card, text="CRIAR NOVA CONTA", width=320, height=55, font=("Inter", 16, "bold"), 
                                           fg_color="white", border_color="#2ecc71", border_width=2, text_color="#2ecc71",
                                           hover_color="#e8f5e9", corner_radius=15, command=self.executar_cadastro)
        self.btn_cadastrar.pack(pady=5)
        self.btn_cadastrar.bind("<Enter>", lambda e: self.btn_cadastrar.configure(text_color="#27ae60"))
        self.btn_cadastrar.bind("<Leave>", lambda e: self.btn_cadastrar.configure(text_color="#2ecc71"))

        self.carregar_preferencias()

    def acao_esqueci_senha(self):
        user = self.entry_user.get()
        if not user:
            messagebox.showwarning("Atenção", "Digite o usuário para validar.")
            return
        
        if recuperar_senha(user):
            messagebox.showinfo("Segurança", "Usuário validado. Por segurança, redefina sua senha com o administrador (Criptografia ativa).")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    def carregar_preferencias(self):
        if os.path.exists(self.prefs_file):
            try:
                with open(self.prefs_file, "r") as f:
                    prefs = json.load(f)
                    if prefs.get("remember"):
                        self.entry_user.insert(0, prefs.get("username", ""))
                        self.check_remember.select()
            except: pass

    def salvar_preferencias(self):
        prefs = {
            "remember": self.check_remember.get(),
            "username": self.entry_user.get() if self.check_remember.get() else ""
        }
        with open(self.prefs_file, "w") as f:
            json.dump(prefs, f)

    def executar_login(self):
        u, s = self.entry_user.get(), self.entry_pass.get()
        if login_usuario(u, s):
            self.salvar_preferencias()
            self.login_success_callback()
        else:
            messagebox.showerror("Erro", "Login ou senha incorretos")

    def executar_cadastro(self):
        u, s = self.entry_user.get(), self.entry_pass.get()
        if not u or not s:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        if cadastrar_usuario(u, s):
            messagebox.showinfo("Sucesso", "Conta criada com criptografia!")
        else:
            messagebox.showerror("Erro", "Usuário já existe")   