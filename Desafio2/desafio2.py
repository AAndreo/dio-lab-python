
def menu()  -> str:
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário 
    [lu] Listar Usuários
    [q] Sair

    => """

    return input(menu)

def depositar(valor:float, saldo:float, /) -> float:
    saldo += valor
    return saldo

def sacar(*, valor:float, saldo:float) -> float:
    saldo -= valor
    return saldo

def extrato(operacao:str, valor:float, lista_extrato:list) -> None:
    lista_extrato.append(f"{operacao}: R$ {valor:.2f}")

def listar_extrato(lista_extrato:list, /, *, saldo:float):
    print("\n================ EXTRATO ================")
    if len(lista_extrato) > 0:
        for o in lista_extrato:
            print(o)
    else:
        print("Não foram realizadas movimentações.")
    print("=========================================")
    print(f"Saldo: R$ {saldo:.2f}")

def criar_usuario(usuarios:dict):

    try:
        cpf = int(input("Informe o CPF (somente número): "))
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return

    usuario = usuarios.get(cpf, "Usuário não encontrado!")

    if usuario == "Usuário não encontrado!":

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuarios[cpf] = {"Nome" : nome, "data_nascimento" : data_nascimento, "endereco" : endereco }

        print("=== Usuário criado com sucesso! ===")

    else:

        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

def listar_usuarios(usuarios:dict) -> None:

        print("\n================ Usuários ================")
        for chave, valor in usuarios.items():
            print(chave, valor)

def criar_conta(AGENCIA:str, contas: dict, usuarios:dict) -> dict:

    try:
        cpf = int(input("Informe o CPF (somente número): "))
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return
    
    usuario = usuarios.get(cpf, "Usuário não encontrado!")

    if usuario == "Usuário não encontrado!":

        print("\n@@@ Usuário não encontrado com esse CPF! @@@")
        return

    else:

        conta = len(contas) + 1
        contas[conta] = {"Agencia" : AGENCIA, "conta" : conta, "usuario" : usuario}

        print("\n=== Conta criada com sucesso! ===")

        return contas

def listar_contas(contas:dict) -> None:

    for chave, valor in contas.items():
        print(chave, valor)

def main():

    saldo = 0
    limite = 500
    lista_extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = {}
    contas = {}

    while True:

        opcao = menu()

        if opcao == "d":

            try:
                valor = float(input('Informe o valor para depósito:'))
            except ValueError:
                print("Valor inválido - Não foi possível realizar a operação!")
            else:
                if valor > 0:
                    saldo = depositar(valor, saldo)
                    extrato("Depósito", valor, lista_extrato)
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
                        saldo = sacar(valor=valor, saldo=saldo)
                        numero_saques += 1
                        extrato("Saque", valor, lista_extrato)
                    else:
                        print("Valor inválido - Não foi possível realizar a operação!")
                
        elif opcao == "e":
            listar_extrato(lista_extrato, saldo=saldo)

        elif opcao == "nc":
            criar_conta(AGENCIA, contas, usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_usuario(usuarios=usuarios)

        elif opcao == "lu":
            listar_usuarios(usuarios=usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()