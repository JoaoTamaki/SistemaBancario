from datetime import date
import datetime

import Banco
from decimal import Decimal

from Usuarios import Usuarios
import tkinter
from tkinter import *
from tkinter import messagebox


class Application:

    def __init__(self, master=None):

        self.limite_valor_saque = 500
        self.limite_saques = 3

        self.usuario = None
        self.data_ultimo_login = None
        self.num_saques_disponivel = 0
        self.saldo = 0
        self.extrato = []
        self.arquivo_extrato = None

        self.root = Tk()
        self.root.title("Janela de Acesso")
        self.root.resizable(width=False, height=False)
        self.fonte = ("Verdana", "8")

        self.root.container15 = Frame(master)
        self.root.container15["pady"] = 10
        self.root.container15.pack()
        self.root.container16 = Frame(master)
        self.root.container16["pady"] = 10
        self.root.container16["padx"] = 40
        self.root.container16.pack()

        self.mensagem = Label(self.root.container15, text="Bem Vindo aos Sistema Bancário JVKT! O que deseja fazer?")
        self.mensagem["font"] = ("Calibri", "9", "bold")
        self.mensagem.pack()

        self.botao_criar_conta = Button(self.root.container16, text="Criar Conta", font=self.fonte,
                                        command=self.tela_criar_usuario)
        self.botao_criar_conta.pack(side=LEFT)

        self.botao_login = Button(self.root.container16, text="Fazer Login", font=self.fonte,
                                  command=self.tela_fazer_login)
        self.botao_login.pack(side=LEFT)

        self.botao_sair = Button(self.root.container16, text="Sair", font=self.fonte,
                                 command=self.root.destroy)
        self.botao_sair.pack(side=RIGHT)

        self.root.mainloop()

    def load_extrato_usuario(self):
        with open(self.arquivo_extrato) as f:
            self.extrato = []
            linha = f.readline().split('\n')[0]
            while linha:
                self.extrato.append(linha)
                linha = f.readline().split('\n')[0]

    def save_info_usuario(self):
        Banco.cursor.execute("""
            UPDATE Usuarios
            SET Data_ultimo_login=?, Num_saques_disponivel=?, Saldo=?
            WHERE Usuario=?
        """, (self.data_ultimo_login, self.num_saques_disponivel, str(self.saldo), self.usuario))
        Banco.conn.commit()
        messagebox.showinfo(title="Transation Info", message="Operação realizada com sucesso!")

        with open(self.arquivo_extrato, "w") as f:
            for i in range(len(self.extrato)):
                f.write(self.extrato[i] + '\n')

    def realiza_deposito(self):
        valor = Decimal(self.root3.txt_deposito.get())
        # somente valores positivos
        if valor > 0:
            # deposito deve ser armazenado em uma variável
            self.saldo = round(float(Decimal(str(self.saldo)) + Decimal(valor)), 2)
            data = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            print(self.extrato)
            print(type(self.extrato))
            self.extrato.append(f"{data} Deposito R$ {valor:.2f}")
            self.save_info_usuario()

            self.root3.destroy()
            self.root2.destroy()
            self.tela_operacoes_bancarias()
            self.root2.lbl_mensagem = Label(self.root2.container_2_1, text='Depósito efetuado com sucesso!')
            self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
            self.root2.lbl_mensagem.pack()

        else:
            self.root3.destroy()
            self.root2.destroy()
            self.tela_operacoes_bancarias()
            self.root2.lbl_mensagem = Label(self.root2.container_2_1,
                                            text='Operação falhou!O valor informado é inválido.')
            self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
            self.root2.lbl_mensagem.pack()

    def realiza_saque(self):
        if self.num_saques_disponivel == 0:
            # se excedeu o número de saques do dia
            self.root3.destroy()
            self.root2.destroy()
            self.tela_operacoes_bancarias()
            self.root2.lbl_mensagem = Label(self.root2.container_2_1,
                                            text='Você excedeu o limite de quantidade de saques hoje. Por favor,'
                                                 'volte amanhã ou fale com o gerente.')
            self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
            self.root2.lbl_mensagem.pack()
        else:
            valor_saque = self.root3.txt_saque.get()
            valor_saque = round(float(valor_saque), 2)
            print(valor_saque)
            if valor_saque > self.saldo:
                # se não tiver saldo
                self.root3.destroy()
                self.root2.destroy()
                self.tela_operacoes_bancarias()
                self.root2.lbl_mensagem = Label(self.root2.container_2_1,
                                                text='Não foi possível sacar o dinheiro por falta de saldo.')
                self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
                self.root2.lbl_mensagem.pack()
            elif valor_saque > self.limite_valor_saque:
                # se exceder o limite de valor de saque
                self.root3.destroy()
                self.root2.destroy()
                self.tela_operacoes_bancarias()
                self.root2.lbl_mensagem = Label(self.root2.container_2_1,
                                                text='Você excedeu o seu limite de valor por saque: R$500,00.'
                                                     'Tente novamente com um valor mais baixo.')
                self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
                self.root2.lbl_mensagem.pack()
            elif valor_saque > 0:
                # saque deve ser armazenado em uma variável
                self.saldo = round(float(Decimal(str(self.saldo)) - Decimal(valor_saque)), 2)
                data = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                self.extrato.append(f"{data} Saque: R$ {valor_saque:.2f}")
                self.num_saques_disponivel -= 1
                self.save_info_usuario()

                self.root3.destroy()
                self.root2.destroy()
                self.tela_operacoes_bancarias()
                self.root2.lbl_mensagem = Label(self.root2.container_2_1, text='Saque efetuado com sucesso!')
                self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
                self.root2.lbl_mensagem.pack()
            else:
                self.root3.destroy()
                self.root2.destroy()
                self.tela_operacoes_bancarias()
                self.root2.lbl_mensagem = Label(self.root2.container_2_1,
                                                text='Operação falhou! O valor informado é inválido.')
                self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
                self.root2.lbl_mensagem.pack()

    def criar_usuario(self):
        user = Usuarios()

        user.nome = self.root1.txt_nome.get()
        user.data_nascimento = self.root1.txt_data_nascimento.get()
        user.cpf = self.root1.txt_cpf.get()
        user.logradouro = self.root1.txt_logradouro.get()
        user.numero = self.root1.txt_numero.get()
        user.bairro = self.root1.txt_bairro.get()
        user.cidade_estado = self.root1.txt_cidade_estado.get()
        user.usuario = self.root1.txt_usuario.get()
        user.senha = self.root1.txt_senha.get()
        user.conf_senha = self.root1.txt_conf_senha.get()

        if (user.senha == user.conf_senha and user.nome != "" and user.data_nascimento != ""
                and user.cpf != "" and user.logradouro != "" and user.numero != "" and user.bairro != ""
                and user.cidade_estado != "" and user.usuario != "" and user.senha != "" and user.conf_senha != ""):
            user.save()
            self.root1.txt_nome.delete(0, END)
            self.root1.txt_data_nascimento.delete(0, END)
            self.root1.txt_cpf.delete(0, END)
            self.root1.txt_logradouro.delete(0, END)
            self.root1.txt_numero.delete(0, END)
            self.root1.txt_bairro.delete(0, END)
            self.root1.txt_cidade_estado.delete(0, END)
            self.root1.txt_usuario.delete(0, END)
            self.root1.txt_senha.delete(0, END)
            self.root1.txt_conf_senha.delete(0, END)
        else:
            messagebox.showerror(title="Register Error", message="Não deixe campos vazios! Preencha todos os campos!")

    def verificar_senha(self):

        usuario = self.root0.txt_usuario_login.get()
        senha = self.root0.txt_senha_login.get()

        Banco.cursor.execute("""
            SELECT * FROM Usuarios
            WHERE (Usuario = ? AND Senha = ?) 
        """, (usuario, senha))
        verify_login = Banco.cursor.fetchone()
        (*_, self.usuario, self.senha, self.data_ultimo_login, self.num_saques_disponivel,
         self.saldo, self.extrato) = verify_login
        try:
            if usuario in verify_login and senha in verify_login:
                messagebox.showinfo(title="Login Info", message="Acesso Confirmado. Bem vindo!")
        except:
            messagebox.showinfo(title="Login Info", message="Acesso Negado. Verifique os dados de"
                                                            "entrada ou se não tem cadastro ainda.")

        if self.data_ultimo_login != str(date.today().strftime("%d/%m/%Y")):
            self.num_saques_disponivel = self.limite_saques

        self.arquivo_extrato = self.extrato
        self.load_extrato_usuario()
        self.tela_operacoes_bancarias()
        print('Login efetuado com sucesso!')

# Telas
# 1
    def tela_criar_usuario(self):
        self.root1 = Toplevel()
        self.root1.title('Crir Usuário')
        self.root1.geometry("800x400")
        self.root1.resizable(width=False, height=False)
        self.root1.grab_set()

        self.root1.container1 = Frame(self.root1)
        self.root1.container1["pady"] = 10
        self.root1.container1.pack()
        self.root1.container2 = Frame(self.root1)
        self.root1.container2["padx"] = 80
        self.root1.container2["pady"] = 5
        self.root1.container2.pack()
        self.root1.container3 = Frame(self.root1)
        self.root1.container3["padx"] = 80
        self.root1.container3["pady"] = 5
        self.root1.container3.pack()
        self.root1.container4 = Frame(self.root1)
        self.root1.container4["padx"] = 80
        self.root1.container4["pady"] = 5
        self.root1.container4.pack()
        self.root1.container5 = Frame(self.root1)
        self.root1.container5["padx"] = 80
        self.root1.container5["pady"] = 5
        self.root1.container5.pack()
        self.root1.container6 = Frame(self.root1)
        self.root1.container6["pady"] = 15
        self.root1.container6.pack()
        self.root1.container7 = Frame(self.root1)
        self.root1.container7["padx"] = 80
        self.root1.container7["pady"] = 5
        self.root1.container7.pack()
        self.root1.container8 = Frame(self.root1)
        self.root1.container8["padx"] = 80
        self.root1.container8["pady"] = 10
        self.root1.container8.pack()
        self.root1.container9 = Frame(self.root1)
        self.root1.container9["padx"] = 80
        self.root1.container9["pady"] = 5
        self.root1.container9.pack()
        self.root1.container10 = Frame(self.root1)
        self.root1.container10["padx"] = 80
        self.root1.container10["pady"] = 5
        self.root1.container10.pack()
        self.root1.container11 = Frame(self.root1)
        self.root1.container11["pady"] = 15
        self.root1.container11.pack()

        # Título
        self.root1.titulo = Label(self.root1.container1, text="Informe os dados :")
        self.root1.titulo["font"] = ("Calibri", "9", "bold")
        self.root1.titulo.pack()

        # Nome
        self.root1.lbl_nome = Label(self.root1.container2, text="Nome:", font=self.fonte, width=10)
        self.root1.lbl_nome.pack(side=LEFT)
        self.root1.txt_nome = Entry(self.root1.container2)
        self.root1.txt_nome["width"] = 62
        self.root1.txt_nome["font"] = self.fonte
        self.root1.txt_nome.pack(side=LEFT)

        # Data de Nascimento
        self.root1.lbl_data_nascimento = Label(self.root1.container3, text="Data de Nascimento:", font=self.fonte,
                                               width=20)
        self.root1.lbl_data_nascimento.pack(side=LEFT)
        self.root1.txt_data_nascimento = Entry(self.root1.container3)
        self.root1.txt_data_nascimento["width"] = 15
        self.root1.txt_data_nascimento["font"] = self.fonte
        self.root1.txt_data_nascimento.pack(side=LEFT)

        # CPF
        self.root1.lbl_cpf = Label(self.root1.container3, text="CPF:", font=self.fonte, width=10)
        self.root1.lbl_cpf.pack(side=LEFT)
        self.root1.txt_cpf = Entry(self.root1.container3)
        self.root1.txt_cpf["width"] = 25
        self.root1.txt_cpf["font"] = self.fonte
        self.root1.txt_cpf.pack(side=LEFT)

        # Logradouro
        self.root1.lbl_logradouro = Label(self.root1.container4, text="Logradouro:", font=self.fonte, width=10)
        self.root1.lbl_logradouro.pack(side=LEFT)
        self.root1.txt_logradouro = Entry(self.root1.container4)
        self.root1.txt_logradouro["width"] = 40
        self.root1.txt_logradouro["font"] = self.fonte
        self.root1.txt_logradouro.pack(side=LEFT)

        self.root1.lbl_numero = Label(self.root1.container4, text="Número:", font=self.fonte, width=10)
        self.root1.lbl_numero.pack(side=LEFT)
        self.root1.txt_numero = Entry(self.root1.container4)
        self.root1.txt_numero["width"] = 10
        self.root1.txt_numero["font"] = self.fonte
        self.root1.txt_numero.pack(side=RIGHT)

        # Outras infos logradouro
        self.root1.lbl_bairro = Label(self.root1.container5, text="Bairro:", font=self.fonte, width=10)
        self.root1.lbl_bairro.pack(side=LEFT)
        self.root1.txt_bairro = Entry(self.root1.container5)
        self.root1.txt_bairro["width"] = 25
        self.root1.txt_bairro["font"] = self.fonte
        self.root1.txt_bairro.pack(side=LEFT)

        self.root1.lbl_cidade_estado = Label(self.root1.container5, text="Cidade/Estado:", font=self.fonte, width=15)
        self.root1.lbl_cidade_estado.pack(side=LEFT)
        self.root1.txt_cidade_estado = Entry(self.root1.container5)
        self.root1.txt_cidade_estado["width"] = 20
        self.root1.txt_cidade_estado["font"] = self.fonte
        self.root1.txt_cidade_estado.pack(side=RIGHT)

        self.root1.lbl_espaco = Label(self.root1.container6, text="")
        self.root1.lbl_espaco["font"] = ("Verdana", "9", "italic")
        self.root1.lbl_espaco.pack()

        # Nome de Usuário
        self.root1.lbl_usuario = Label(self.root1.container7, text="Usuário:", font=self.fonte, width=20)
        self.root1.lbl_usuario.pack(side=LEFT)
        self.root1.txt_usuario = Entry(self.root1.container7)
        self.root1.txt_usuario["width"] = 25
        self.root1.txt_usuario["font"] = self.fonte
        self.root1.txt_usuario.pack(side=LEFT)

        # Senha
        self.root1.lbl_senha = Label(self.root1.container8, text="Senha:", font=self.fonte, width=20)
        self.root1.lbl_senha.pack(side=LEFT)
        self.root1.txt_senha = Entry(self.root1.container8)
        self.root1.txt_senha["width"] = 25
        self.root1.txt_senha["show"] = "*"
        self.root1.txt_senha["font"] = self.fonte
        self.root1.txt_senha.pack(side=LEFT)

        # Confirmação de Senha
        self.root1.lbl_conf_senha = Label(self.root1.container9, text="Confirmar Senha:", font=self.fonte, width=20)
        self.root1.lbl_conf_senha.pack(side=LEFT)
        self.root1.txt_conf_senha = Entry(self.root1.container9)
        self.root1.txt_conf_senha["width"] = 25
        self.root1.txt_conf_senha["show"] = "*"
        self.root1.txt_conf_senha["font"] = self.fonte
        self.root1.txt_conf_senha.pack(side=LEFT)

        self.root1.botao_criar = Button(self.root1.container10, text="Criar", font=self.fonte, width=12,
                                        command=self.criar_usuario)
        self.root1.botao_criar.pack(side=LEFT)

        self.root1.botao_voltar = Button(self.root1.container10, text="Voltar", font=self.fonte, width=12,
                                         command=self.root1.destroy)
        self.root1.botao_voltar.pack(side=LEFT)

        self.root1.lbl_msg = Label(self.root1.container11, text="", font=("Verdana", "9", "italic"))
        self.root1.lbl_msg.pack()

# 0
    def tela_fazer_login(self):

        self.root0 = Toplevel()
        self.root0.title('Fazer Login')
        self.root0.geometry("400x200")
        self.root0.resizable(width=False, height=False)
        self.root0.grab_set()

        self.root0.container61 = Frame(self.root0)
        self.root0.container61["pady"] = 10
        self.root0.container61.pack()
        self.root0.container62 = Frame(self.root0)
        self.root0.container62["pady"] = 10
        self.root0.container62["padx"] = 40
        self.root0.container62.pack()
        self.root0.container63 = Frame(self.root0)
        self.root0.container63["pady"] = 10
        self.root0.container63["padx"] = 40
        self.root0.container63.pack()
        self.root0.container64 = Frame(self.root0)
        self.root0.container64["pady"] = 10
        self.root0.container64["padx"] = 40
        self.root0.container64.pack()

        self.root0.mensagem = Label(self.root0.container61, text="Faça o seu Login no Sistema Bancário JVKT!")
        self.root0.mensagem["font"] = ("Calibri", "9", "bold")
        self.root0.mensagem.pack()

        self.root0.lbl_usuario_login = Label(self.root0.container62, text="Usuário:", font=self.fonte, width=20)
        self.root0.lbl_usuario_login.pack(side=LEFT)
        self.root0.txt_usuario_login = Entry(self.root0.container62)
        self.root0.txt_usuario_login["width"] = 25
        self.root0.txt_usuario_login["font"] = self.fonte
        self.root0.txt_usuario_login.pack(side=LEFT)

        self.root0.lbl_senha_login = Label(self.root0.container63, text="Senha:", font=self.fonte, width=20)
        self.root0.lbl_senha_login.pack(side=LEFT)
        self.root0.txt_senha_login = Entry(self.root0.container63)
        self.root0.txt_senha_login["width"] = 25
        self.root0.txt_senha_login["show"] = "*"
        self.root0.txt_senha_login["font"] = self.fonte
        self.root0.txt_senha_login.pack(side=LEFT)

        self.root0.botao_login = Button(self.root0.container64, text="Entrar", font=self.fonte,
                                        command=self.verificar_senha)
        self.root0.botao_login.pack(side=LEFT)

        self.root0.botao_criar_conta = Button(self.root0.container64, text="Criar Conta", font=self.fonte,
                                              command=self.tela_criar_usuario)
        self.root0.botao_criar_conta.pack(side=LEFT)

        self.root0.botao_volte_menu = Button(self.root0.container64, text="Sair", font=self.fonte,
                                             command=self.root0.destroy)
        self.root0.botao_volte_menu.pack(side=RIGHT)

# 3
    def tela_deposito(self):

        self.root3 = Toplevel()
        self.root3.title('Depósito')
        self.root3.configure(background='lightblue')
        self.root3.geometry("510x40")
        self.root3.resizable(width=False, height=False)
        self.root3.transient(self.root2)
        self.root3.grab_set()

        self.root3.container20 = Frame(self.root3)
        self.root3.container20["pady"] = 10
        self.root3.container20["padx"] = 40
        self.root3.container20.pack()

        self.root3.lbl_deposito = Label(self.root3.container20, text="Valor do Depósito:", font=self.fonte, width=20)
        self.root3.lbl_deposito.pack(side=LEFT)
        self.root3.txt_deposito = Entry(self.root3.container20)
        self.root3.txt_deposito["width"] = 25
        self.root3.txt_deposito["font"] = self.fonte
        self.root3.txt_deposito.pack(side=LEFT)

        self.root3.botao_voltar = Button(self.root3.container20, text="Voltar", font=self.fonte,
                                         command=self.root3.destroy)
        self.root3.botao_voltar.pack(side=RIGHT)

        self.root3.botao_depositar = Button(self.root3.container20, text="Depositar", font=self.fonte,
                                            command=self.realiza_deposito)
        self.root3.botao_depositar.pack(side=RIGHT)

# 3
    def tela_saque(self):

        self.root3 = Toplevel()
        self.root3.title('Saque')
        self.root3.configure(background='lightblue')
        self.root3.geometry("490x40")
        self.root3.resizable(width=False, height=False)
        self.root3.transient(self.root2)
        self.root3.grab_set()

        self.root3.container20 = Frame(self.root3)
        self.root3.container20["pady"] = 10
        self.root3.container20["padx"] = 40
        self.root3.container20.pack()

        self.root3.lbl_saque = Label(self.root3.container20, text="Valor do Saque:", font=self.fonte, width=20)
        self.root3.lbl_saque.pack(side=LEFT)
        self.root3.txt_saque = Entry(self.root3.container20)
        self.root3.txt_saque["width"] = 25
        self.root3.txt_saque["font"] = self.fonte
        self.root3.txt_saque.pack(side=LEFT)

        self.root3.botao_voltar = Button(self.root3.container20, text="Voltar", font=self.fonte,
                                         command=self.root3.destroy)
        self.root3.botao_voltar.pack(side=RIGHT)

        self.root3.botao_sacar = Button(self.root3.container20, text="Sacar", font=self.fonte,
                                        command=self.realiza_saque)
        self.root3.botao_sacar.pack(side=RIGHT)

    def tela_extrato(self):
        self.root3 = Toplevel()
        self.root3.title('Extrato')
        self.root3.geometry("400x400")
        self.root3.resizable(width=False, height=False)
        self.root3.transient(self.root2)
        self.root3.grab_set()

        self.root3.container_3_1 = Frame(self.root3)
        self.root3.container_3_1["pady"] = 10
        self.root3.container_3_1.pack()
        self.root3.lbl_mensagem = Label(self.root3.container_3_1, text='================ EXTRATO ================')
        self.root3.lbl_mensagem["font"] = ("Calibri", "9", "bold")
        self.root3.lbl_mensagem.pack()

        for i in range(len(self.extrato)):
            print(self.extrato[i])
            self.root3.mensagem = Label(self.root3.container_3_1, text=self.extrato[i])
            self.root3.mensagem["font"] = ("Calibri", "9", "bold")
            self.root3.mensagem.pack()

        self.root3.down_mensagem = Label(self.root3.container_3_1, text='==========================================')
        self.root3.down_mensagem["font"] = ("Calibri", "9", "bold")
        self.root3.down_mensagem.pack()

# 2
    def tela_operacoes_bancarias(self):
        self.root2 = Toplevel()
        self.root2.title('Operações Bancárias')
        self.root2.configure(background='lightblue')
        self.root2.geometry("600x400")
        self.root2.resizable(width=False, height=False)
        self.root2.transient(self.root0)
        self.root2.grab_set()

        self.root2.container_2_1 = Frame(self.root2)
        self.root2.container_2_1["pady"] = 10
        self.root2.container_2_1.pack()
        self.root2.lbl_usuario = Label(self.root2.container_2_1, text=f'Olá {self.usuario}!')
        self.root2.lbl_usuario["font"] = ("Calibri", "9", "bold")
        self.root2.lbl_usuario.pack()
        self.root2.lbl_mensagem = Label(self.root2.container_2_1, text='Seu Saldo: ')
        self.root2.lbl_mensagem["font"] = ("Calibri", "9", "bold")
        self.root2.lbl_mensagem.pack()
        self.root2.mensagem = Label(self.root2.container_2_1, text=f'R$ {self.saldo:.2f}')
        self.root2.mensagem["font"] = ("Calibri", "9", "bold")
        self.root2.mensagem.pack()

        self.root2.botao_deposito = tkinter.Button(self.root2, text='Depósito', command=self.tela_deposito)
        self.root2.botao_deposito.place(relx=0.3, rely=0.3)
        self.root2.botao_saque = tkinter.Button(self.root2, text='Saque', command=self.tela_saque)
        self.root2.botao_saque.place(relx=0.3, rely=0.7)
        self.root2.botao_extrato = tkinter.Button(self.root2, text='Extrato', command=self.tela_extrato)
        self.root2.botao_extrato.place(relx=0.7, rely=0.3)
        self.root2.botao_sair = tkinter.Button(self.root2, text='Sair', command=self.root2.destroy)
        self.root2.botao_sair.place(relx=0.7, rely=0.7)


def main():

    Application()


if __name__ == '__main__':
    main()
