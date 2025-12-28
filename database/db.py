import sqlite3
import bcrypt

def conectar():
    return sqlite3.connect("finance_pro.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # Tabela de transações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- FUNÇÕES DE USUÁRIO (SEGURANÇA) ---

def cadastrar_usuario(usuario, senha_pura):
    if not usuario or not senha_pura:
        return False
    conn = conectar()
    cursor = conn.cursor()
    
    senha_bytes = senha_pura.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", 
                       (usuario, senha_hash.decode('utf-8')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_usuario(usuario, senha_digitada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        try:
            senha_hash_banco = resultado[0].encode('utf-8')
            if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash_banco):
                return True
        except:
            return False
    return False

def recuperar_senha(usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario,))
    existe = cursor.fetchone()
    conn.close()
    return True if existe else False

# --- FUNÇÕES DE TRANSAÇÕES (EXIGIDAS PELA MAIN_WINDOW) ---

def salvar_transacao(tipo, valor, categoria, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transacoes (tipo, valor, categoria, data) VALUES (?, ?, ?, ?)",
                   (tipo, valor, categoria, data))
    conn.commit()
    conn.close()

def carregar_transacoes(tipo=None):
    conn = conectar()
    cursor = conn.cursor()
    if tipo:
        cursor.execute("SELECT * FROM transacoes WHERE tipo = ?", (tipo,))
    else:
        cursor.execute("SELECT * FROM transacoes")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_transacao(id_transacao):
    """Função que estava faltando para resolver o ImportError"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()