menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
lista_extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(valor:float, saldo:float) -> float:
    saldo += valor
    return saldo

def sacar(valor:float, saldo:float) -> float:
    saldo -= valor
    return saldo

def extrato(operacao:str) -> None:
    lista_extrato.append(f"{operacao}: R$ {valor:.2f}")

def listar_extrato():
    print("\n================ EXTRATO ================")
    if len(lista_extrato) > 0:
        for o in lista_extrato:
            print(o)
    else:
        print("Não foram realizadas movimentações.")
    print("=========================================")
    print(f"Saldo: R$ {saldo:.2f}")

while True:

    opcao = input(menu)

    if opcao == "d":

        try:
            valor = float(input('Informe o valor para depósito:'))
        except ValueError:
            print("Valor inválido - Não foi possível realizar a operação!")
        else:
            if valor > 0:
                saldo = depositar(valor, saldo)
                extrato("Depósito")
            else:
                print("Valor inválido - Não foi possível realizar a operação!")

    elif opcao == "s":
        try:
            valor = float(input('Informe o valor para saque:'))
        except ValueError:
            print("Valor inválido - Não foi possível realizar a operação!")
        else:
            if numero_saques >= LIMITE_SAQUES:
                print("Limite de saques diários (3) excedido - Não foi possível realizar a operação!")
            elif valor > limite:
                print("Valor limite para saques excedido - Não foi possível realizar a operação!")
            elif valor > saldo:
                print("Saldo insuficiente para o valor do saque - Não foi possível realizar a operação!")
            else:
                if valor > 0:
                    saldo = sacar(valor, saldo)
                    numero_saques += 1
                    extrato("Saque")
                else:
                    print("Valor inválido - Não foi possível realizar a operação!")
            
    elif opcao == "e":
        listar_extrato()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
