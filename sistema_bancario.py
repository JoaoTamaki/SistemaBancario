from datetime import date
import datetime


def realiza_deposito(saldo, extrato, /):
    valor = round(float(input("Informe o valor do depósito: ")), 2)
# somente valores positivos
    if valor > 0:
        # deposito deve ser armazenado em uma variável
        saldo = round(saldo+valor-0.005, 2)
        data = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        extrato.append(f"{data} Deposito R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo


def realiza_saque(*, saldo, extrato, num_saques_disponivel, limite_valor_saque):
    if num_saques_disponivel == 0:
        # se excedeu o número de saques do dia
        print("Você excedeu o limite de quantidade de saques hoje. Por favor, volte amanhã ou fale com o gerente.")
    else:
        valor_saque = round(float(input("Informe o valor do saque: ")), 2)
        print(valor_saque)
        if valor_saque > saldo:
            # se não tiver saldo
            print("Não foi possível sacar o dinheiro por falta de saldo.")
        elif valor_saque > limite_valor_saque:
            # se exceder o limite de valor de saque
            print("Você excedeu o seu limite de valor por saque: R$500,00. Tente novamente com um valor mais baixo.")
        elif valor_saque > 0:
            # saque deve ser armazenado em uma variável
            saldo = round(saldo - valor_saque, 2)
            data = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            extrato.append(f"{data} Saque: R$ {valor_saque:.2f}")
            num_saques_disponivel -= 1
        else:
            print("Operação falhou! O valor informado é inválido.")

    return saldo, num_saques_disponivel


def imprime_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    for i in range(len(extrato)):
        print(extrato[i])
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def load_info_usuario(arquivo, limite_saques):
    with open(arquivo) as f:
        data_salva = f.readline().split('\n')[0]
        num_saques_disponivel = f.readline().split('\n')[0]
        if data_salva != str(date.today().strftime("%d/%m/%Y")):
            num_saques_disponivel = limite_saques

        saldo = f.readline().split('\n')[0]
        extrato = []
        linha = f.readline().split('\n')[0]
        while linha:
            extrato.append(linha)
            linha = f.readline().split('\n')[0]

    return int(num_saques_disponivel), float(saldo), extrato


def save_info_usuario(arquivo, limite_saques, saldo, extrato):
    with open(arquivo, "w") as f:
        f.write(date.today().strftime("%d/%m/%Y")+'\n')
        f.write(str(limite_saques)+'\n')
        f.write(f"{saldo:.2f}\n")
        for i in range(len(extrato)):
            f.write(extrato[i]+'\n')


def main():

    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """
    # limite máximo de cada saque: 500,00
    arquivo = 'usuario_unico.txt'
    limite_valor_saque = 500
    limite_saques = 3
    num_saques_disponivel, saldo, extrato = load_info_usuario(arquivo, limite_saques)

    while True:
        opcao = input(menu)
        if opcao == "d":
            saldo = realiza_deposito(saldo, extrato)
        elif opcao == "s":
            saldo, num_saques_disponivel = realiza_saque(saldo=saldo, extrato=extrato,
                                                         num_saques_disponivel=num_saques_disponivel,
                                                         limite_valor_saque=limite_valor_saque)
        elif opcao == "e":
            imprime_extrato(saldo, extrato=extrato)
        elif opcao == "q":
            save_info_usuario(arquivo, num_saques_disponivel, saldo, extrato)
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == '__main__':
    main()
