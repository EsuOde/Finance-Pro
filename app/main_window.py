import customtkinter as ctk
from database.db import salvar_transacao, carregar_transacoes, deletar_transacao
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, logout_callback):
        super().__init__(parent, fg_color="#f0f2f5")
        self.logout_callback = logout_callback

        # Configurações de Categorias
        self.cat_despesas = ["Alimentação", "Lazer", "Transporte", "Saúde", "Contas", "Outros"]
        self.cat_receitas = ["Salário", "Investimento", "Extra", "Outros"]

        # Carregar dados iniciais do banco
        self.dados_despesas = carregar_transacoes("Despesas")
        self.dados_receitas = carregar_transacoes("Receitas")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="white", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="FINANCE PRO", font=("Inter", 22, "bold"), text_color="#4a90e2").pack(pady=40)
        
        self.btn_dash = self.criar_item_menu("📊  Dashboard", self.selecionar_dash)
        self.btn_desp = self.criar_item_menu("📉  Despesas", self.selecionar_desp)
        self.btn_rece = self.criar_item_menu("📈  Receitas", self.selecionar_rece)

        ctk.CTkButton(self.sidebar, text="SAIR", fg_color="#e74c3c", hover_color="#c0392b", 
                      font=("Inter", 13, "bold"), command=self.logout_callback).pack(side="bottom", pady=20, padx=20, fill="x")

        # --- CONTAINER DE TELAS ---
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        self.telas = {
            "Dash": self.criar_dashboard(),
            "Desp": self.criar_financeira("Despesas", "#e74c3c", self.dados_despesas, self.cat_despesas),
            "Rece": self.criar_financeira("Receitas", "#2ecc71", self.dados_receitas, self.cat_receitas)
        }
        self.selecionar_dash()

    def criar_item_menu(self, txt, cmd):
        btn = ctk.CTkButton(self.sidebar, text=txt, anchor="w", fg_color="transparent", text_color="#34495e", 
                            hover_color="#f0f2f5", font=("Inter", 14, "bold"), height=45, command=cmd)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def criar_dashboard(self):
        view = ctk.CTkFrame(self.container, fg_color="transparent")
        ctk.CTkLabel(view, text="Visão Geral", font=("Inter", 32, "bold"), text_color="#2c3e50").pack(anchor="w", pady=(0, 25))
        
        cards = ctk.CTkFrame(view, fg_color="transparent")
        cards.pack(fill="x")
        cards.columnconfigure((0,1,2), weight=1)

        self.card_rec = self.add_card(cards, "RECEITAS", "#2ecc71", 0)
        self.card_des = self.add_card(cards, "DESPESAS", "#e74c3c", 1)
        self.card_sal = self.add_card(cards, "SALDO TOTAL", "#4a90e2", 2)

        self.frame_grafico = ctk.CTkFrame(view, fg_color="white", corner_radius=25)
        self.frame_grafico.pack(fill="both", expand=True, pady=25)
        return view

    def add_card(self, p, t, c, col):
        f = ctk.CTkFrame(p, fg_color="white", corner_radius=20)
        f.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(f, text=t, font=("Inter", 12, "bold"), text_color="#95a5a6").pack(pady=(20,0), padx=25, anchor="w")
        lbl = ctk.CTkLabel(f, text="R$ 0,00", font=("Inter", 26, "bold"), text_color=c)
        lbl.pack(pady=(5,20), padx=25, anchor="w")
        return lbl

    def desenhar_grafico(self, r, d):
        for w in self.frame_grafico.winfo_children(): w.destroy()
        if r <= 0 and d <= 0:
            ctk.CTkLabel(self.frame_grafico, text="Adicione movimentações para ver o gráfico", 
                         font=("Inter", 15), text_color="#7f8c8d").place(relx=0.5, rely=0.5, anchor="center")
            return
        try:
            fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
            fig.patch.set_facecolor('white')
            ax.pie([max(r, 0.01), max(d, 0.01)], labels=['Receitas', 'Despesas'], colors=['#2ecc71', '#e74c3c'], 
                   autopct='%1.1f%%', startangle=140, pctdistance=0.85)
            ax.add_artist(plt.Circle((0,0), 0.70, fc='white'))
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
            plt.close(fig)
        except: pass

    def criar_financeira(self, tipo, cor, lista, cats):
        view = ctk.CTkFrame(self.container, fg_color="transparent")
        ctk.CTkLabel(view, text=tipo, font=("Inter", 30, "bold"), text_color="#2c3e50").pack(anchor="w", pady=(0, 20))
        
        # BARRA DE INPUTS COM CONTRASTE MELHORADO
        inp = ctk.CTkFrame(view, fg_color="white", corner_radius=15)
        inp.pack(fill="x", pady=(0, 20))
        
        e_n = ctk.CTkEntry(inp, placeholder_text="Descrição (ex: Aluguel)", width=250, height=45,
                           fg_color="#f8f9fa", border_color="#dcdde1", text_color="#2c3e50", 
                           font=("Inter", 13), corner_radius=10)
        e_n.pack(side="left", padx=15, pady=15)
        
        e_v = ctk.CTkEntry(inp, placeholder_text="R$ 0,00", width=120, height=45,
                           fg_color="#f8f9fa", border_color="#dcdde1", text_color="#2c3e50", 
                           font=("Inter", 13, "bold"), corner_radius=10)
        e_v.pack(side="left", padx=5)
        
        e_c = ctk.CTkOptionMenu(inp, values=cats, fg_color="#4a90e2", button_color="#357abd",
                                font=("Inter", 12, "bold"), height=45, corner_radius=10)
        e_c.pack(side="left", padx=5)
        
        ctk.CTkButton(inp, text="ADICIONAR", fg_color="#2ecc71" if tipo == "Receitas" else "#e74c3c", 
                      font=("Inter", 13, "bold"), width=140, height=45, corner_radius=10,
                      command=lambda: self.acao_add(e_n, e_v, e_c, scr, lista, cor, tipo)).pack(side="right", padx=15)

        scr = ctk.CTkScrollableFrame(view, fg_color="transparent", height=450)
        scr.pack(fill="both", expand=True)
        
        self.renderizar_lista(scr, lista, cor, tipo)
        return view

    def acao_add(self, e_n, e_v, e_c, scr, lista, cor, tipo):
        try:
            n, v, c = e_n.get(), float(e_v.get().replace(',','.')), e_c.get()
            if not n: return
            salvar_transacao(tipo, n, v, c)
            lista.append({"nome": n, "valor": v, "categoria": c})
            self.renderizar_lista(scr, lista, cor, tipo)
            e_n.delete(0, 'end'); e_v.delete(0, 'end')
            if hasattr(self, 'card_rec'): self.atualizar_valores_dashboard()
        except: pass

    def renderizar_lista(self, scr, lista, cor, tipo):
        for w in scr.winfo_children(): w.destroy()
        for i, it in enumerate(lista):
            r = ctk.CTkFrame(scr, fg_color="white", corner_radius=12)
            r.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(r, text=f"{it['nome']}", font=("Inter", 15, "bold"), text_color="#2c3e50").pack(side="left", padx=(20, 5))
            ctk.CTkLabel(r, text=f"• {it['categoria']}", font=("Inter", 13), text_color="#95a5a6").pack(side="left")
            
            ctk.CTkButton(r, text="Excluir", width=70, height=30, fg_color="#fee2e2", text_color="#ef4444", 
                          hover_color="#fecaca", font=("Inter", 11, "bold"),
                          command=lambda idx=i: self.acao_del(idx, scr, lista, cor, tipo)).pack(side="right", padx=15)
            
            ctk.CTkLabel(r, text=f"R$ {it['valor']:,.2f}", text_color=cor, font=("Inter", 15, "bold")).pack(side="right", padx=10)

    def acao_del(self, idx, scr, lista, cor, tipo):
        it = lista.pop(idx)
        deletar_transacao(tipo, it['nome'], it['valor'], it['categoria'])
        self.renderizar_lista(scr, lista, cor, tipo)
        self.atualizar_valores_dashboard()

    def selecionar_dash(self): self.trocar_tela("Dash")
    def selecionar_desp(self): self.trocar_tela("Desp")
    def selecionar_rece(self): self.trocar_tela("Rece")

    def atualizar_valores_dashboard(self):
        tr = sum(i['valor'] for i in self.dados_receitas)
        td = sum(i['valor'] for i in self.dados_despesas)
        if hasattr(self, 'card_rec'):
            self.card_rec.configure(text=f"R$ {tr:,.2f}")
            self.card_des.configure(text=f"R$ {td:,.2f}")
            self.card_sal.configure(text=f"R$ {tr-td:,.2f}")
            self.desenhar_grafico(tr, td)

    def trocar_tela(self, nome):
        for t in self.telas.values(): t.pack_forget()
        self.telas[nome].pack(fill="both", expand=True)
        self.atualizar_valores_dashboard()