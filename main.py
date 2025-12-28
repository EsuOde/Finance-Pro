import customtkinter as ctk
from app.welcome_screen import WelcomeScreen
from app.main_window import MainWindow
from database.db import criar_tabelas 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Finance Pro")
        self.geometry("1100x700")
        
        # Inicia o banco de dados e cria as colunas novas (incluindo Categoria)
        criar_tabelas()

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Começa sempre pela tela de login
        self.mostrar_login()

    def mostrar_login(self):
        # Limpa o que estiver na tela antes de mostrar o login
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.welcome_screen = WelcomeScreen(self.container, self.mostrar_dashboard)
        self.welcome_screen.pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        # Limpa o login e carrega a tela principal
        for widget in self.container.winfo_children():
            widget.destroy()

        self.main_screen = MainWindow(self.container, self.mostrar_login)
        self.main_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()