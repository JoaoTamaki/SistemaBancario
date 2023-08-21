from tkinter import messagebox
from datetime import date
import Banco


class Usuarios(object):

    def __init__(self, nome="", data_nascimento="", cpf="", logradouro="", numero="", bairro="", cidade_estado="",
                 usuario="", senha="", data_ultimo_login=date.today().strftime("%d/%m/%Y"), num_saques_disponivel=3,
                 saldo=0, extrato="usuario_"):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade_estado = cidade_estado
        self.usuario = usuario
        self.senha = senha
        self.data_ultimo_login = data_ultimo_login
        self.num_saques_disponivel = num_saques_disponivel
        self.saldo = saldo
        self.extrato = extrato

    def save(self):
        arquivo = self.extrato + self.usuario + ".txt"
        Banco.cursor.execute("""
            INSERT INTO Usuarios(Nome, DataNascimento, Cpf, Logradouro, Numero, Bairro, Cidade_estado, Usuario, Senha,
            Data_ultimo_login, Num_saques_disponivel, Saldo, Extrato) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (self.nome, self.data_nascimento, self.cpf, self.logradouro, self.numero, self.bairro,
                              self.cidade_estado, self.usuario, self.senha, self.data_ultimo_login,
                              self.num_saques_disponivel, self.saldo, arquivo))
        Banco.conn.commit()
        messagebox.showinfo(title="Register Info", message="Conta criada com sucesso!")
        arquivo = open(arquivo, 'a')
        arquivo.close()
