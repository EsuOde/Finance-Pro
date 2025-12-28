import customtkinter as ctk


class Login(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        ctk.CTkLabel(seimport sqlite3

def conectar_db():
    return sqlite3.connect('finance_pro.db')

def criar_tabelas():
    conn = conectar_db()
    cursor = conn.cursor()
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password TEXT
        )
    """)
    # Tabela de Transações com a nova coluna CATEGORIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tipo TEXT, 
            descricao TEXT, 
            valor REAL, 
            categoria TEXT
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_usuario(username, password):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def login_usuario(username, password):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def salvar_transacao(tipo, descricao, valor, categoria):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, categoria) VALUES (?, ?, ?, ?)", 
                   (tipo, descricao, valor, categoria))
    conn.commit()
    conn.close()

def carregar_transacoes(tipo):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT descricao, valor, categoria FROM transacoes WHERE tipo = ?", (tipo,))
    rows = cursor.fetchall()
    conn.close()
    return [{"nome": row[0], "valor": row[1], "categoria": row[2]} for row in rows]

def deletar_transacao(tipo, descricao, valor, categoria):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM transacoes 
        WHERE id = (SELECT id FROM transacoes WHERE tipo=? AND descricao=? AND valor=? AND categoria=? LIMIT 1)
    """, (tipo, descricao, valor, categoria))
    conn.commit()
    conn.close()lf, text="Login", font=("Arial", 32)).pack(pady=40)

        ctk.CTkButton(
            self,
            text="Entrar",
            command=self.controller.mostrar_dashboard
        ).pack(pady=20)
