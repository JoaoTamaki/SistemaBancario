import pandas as pd
from datetime import date

class Usuarios(object):

    def __init__(self, nome="", data_nascimento="", cpf="", logradouro="", numero="", bairro="", cidade_estado="", usuario="", senha="", data_ultimo_login=date.today().strftime("%d/%m/%Y"), num_saques_disponivel=3, saldo=0, extrato=[]):
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

        dados = [[self.nome, self.data_nascimento, self.cpf, self.logradouro, self.numero, self.bairro,
                 self.cidade_estado, self.usuario, self.senha, self.data_ultimo_login, self.num_saques_disponivel,
                 self.saldo, f"usuario_{self.usuario}.txt"]]
        df = pd.DataFrame(dados,
                          columns=['nome', 'data_nascimento', 'cpf', 'logradouro', 'numero', 'bairro', 'cidade_estado',
                                   'usuario', 'senha', 'data_ultimo_login', 'num_saques_disponivel', 'saldo',
                                   'extrato'])
        arquivo = open(f"usuario_{self.usuario}.txt", 'a')
        usuarios = pd.read_csv("usuarios.csv")
        usuarios = pd.concat([usuarios, df])
        usuarios.to_csv("usuarios.csv", index = False)
