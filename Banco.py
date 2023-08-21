import sqlite3
conn = sqlite3.connect('users.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    DataNascimento TEXT NOT NULL,
    Cpf INTEGER NOT NULL,
    Logradouro TEXT NOT NULL,
    Numero INTEGER NOT NULL,
    Bairro TEXT NOT NULL,
    Cidade_estado TEXT NOT NULL,
    Usuario TEXT NOT NULL,
    Senha TEXT NOT NULL,
    Data_ultimo_login TEXT NOT NULL, 
    Num_saques_disponivel INTEGER NOT NULL,
    Saldo FLOAT NOT NULL,
    Extrato TEXT NOT NULL
);
""")
