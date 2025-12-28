from database.db import conectar

conn = conectar()
cursor = conn.cursor()

cursor.execute("SELECT * FROM transacoes")
rows = cursor.fetchall()

print("DADOS NO BANCO:")
for r in rows:
    print(r)

conn.close()
