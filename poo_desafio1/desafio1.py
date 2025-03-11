from datetime import datetime
from abc import ABC, abstractmethod

class Cliente:

    def __init__(self, endereco:str):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)                

class PessoaFisica(Cliente):

    def __init__(self, nome:str, cpf:str, data_nascimento:datetime, endereco:str):
        super().__init__(endereco=endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def __str__(self):
        return print(f"CPF: {self._cpf} Nome: {self._nome} Nascimento: {self._data_nascimento}")

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Historico:

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )   

class Conta:

    def __init__(self, numero:int, cliente:PessoaFisica):
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()    

    @property
    def agencia(self):
        return self._agencia

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico      
    
    @classmethod
    def nova_conta(cls, numero:int, cliente:PessoaFisica):

        return cls(numero, cliente)
    
    def depositar(self, valor:float)->bool:
        if valor > 0:     
            self._saldo += valor
            return True
        else:
            print("Valor inválido - Não foi possível realizar a operação!")
            return False

class ContaCorrente(Conta):

    def __init__(self, numero:int, cliente:PessoaFisica, limite:float=500, limite_saques:float=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

            
    def sacar(self, valor:float):

        qtd_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Sacar.__name__]
        )

        if qtd_saques >= self._limite_saques:
            print("Limite de saques diários (3) excedido - Não foi possível realizar a operação!")
        elif valor > self._limite:
            print("Valor limite para saques excedido - Não foi possível realizar a operação!")
        elif valor > self.saldo:
            print("Saldo insuficiente para o valor do saque - Não foi possível realizar a operação!")
        else:
            if valor > 0:
                self._saldo -= valor
                return True

            else:
                print("Valor inválido - Não foi possível realizar a operação!")     

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t{self.saldo}
        """        
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )    

class Transacao(ABC): # Interface
    
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass        

class Deposito(Transacao):

    def __init__(self, valor:float):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao = conta.depositar(self._valor)

        if transacao:
            conta.historico.adicionar_transacao(self)
    
class Sacar(Transacao):

    def __init__(self, valor:float):
        super().__init__()
        self._valor = valor        

    @property
    def valor(self):
        return self._valor    

    def registrar(self, conta):
        transacao = conta.sacar(self._valor)

        if transacao:
            conta.historico.adicionar_transacao(self)


    
def buscar_cliente(cpf:int , clientes:list)->PessoaFisica:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

    
def novo_cliente(clientes:list)->None:

    try:
        cpf = int(input("Informe o CPF (somente número): "))
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return

    cliente = buscar_cliente(cpf, clientes)
    if not cliente:

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome,cpf,data_nascimento,endereco)

        clientes.append(cliente)

        print("=== Usuário criado com sucesso! ===")

    else:

        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
def listar_clientes(clientes:list)-> None:

    for cliente in clientes:
        print(f"CPF: {cliente.cpf} Nome: {cliente.nome} Nascimento: {cliente.data_nascimento}")

def criar_conta(numero_conta:int, clientes: list, contas:list) -> None:

    try:
        cpf = int(input("Informe o CPF (somente número): "))
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return

    cliente = buscar_cliente(cpf, clientes)

    if not cliente:

        print("\n@@@ Usuário não encontrado com esse CPF! @@@")
        return

    else:

        conta = ContaCorrente.nova_conta(numero_conta, cliente)
        contas.append(conta)
        cliente.adicionar_conta(conta)

        print("\n=== Conta criada com sucesso! ===")    

def listar_contas(contas:list):
    for conta in contas:
        print("=" * 100)
        print(str(conta))

def buscar_conta(numero_conta:int, cliente:PessoaFisica)->ContaCorrente:

    conta = [conta for conta in cliente.contas if conta.numero == numero_conta]
    return conta[0] if conta else None


def depositar(clientes:list):
    try:
        cpf = int(input("Informe o CPF (somente número): "))
        cliente = buscar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Usuário não encontrado com esse CPF! @@@")
            return
        
        nro_conta = int(input("Informe o número da conta (somente número): "))

        conta = buscar_conta(nro_conta, cliente)

        if not conta:
            print("\n@@@ Conta não encontrada para esse CPF! @@@")
            return
                
        valor = float(input('Informe o valor para depósito:'))

        if valor > 0:
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)
            print("Depósito efetuado com sucesso!")
        else:
            print("Valor inválido - Não foi possível realizar a operação!")
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return

def sacar(clientes:list):
    try:
        cpf = int(input("Informe o CPF (somente número): "))
        cliente = buscar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Usuário não encontrado com esse CPF! @@@")
            return
        
        nro_conta = int(input("Informe o número da conta (somente número): "))

        conta = buscar_conta(nro_conta, cliente)

        if not conta:
            print("\n@@@ Conta não encontrada para esse CPF! @@@")
            return
                
        valor = float(input('Informe o valor para saque:'))

        if valor > 0:
            transacao = Sacar(valor)
            cliente.realizar_transacao(conta, transacao)
            print("Saque efetuado com sucesso!")
        else:
            print("Valor inválido - Não foi possível realizar a operação!")
    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return    

def extrato(clientes:list):
    try:
        cpf = int(input("Informe o CPF (somente número): "))
        cliente = buscar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Usuário não encontrado com esse CPF! @@@")
            return
        
        nro_conta = int(input("Informe o número da conta (somente número): "))

        conta = buscar_conta(nro_conta, cliente)

        if not conta:
            print("\n@@@ Conta não encontrada para esse CPF! @@@")
            return
        
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} - {transacao['data']}"

        print(extrato)
        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")

    except ValueError:
        print("Valor inválido - Não foi possível realizar a operação!")
        return


def menu()  -> str:
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Cliente
    [lu] Listar Clientes
    [q] Sair

    => """

    return input(menu)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            extrato(clientes)
 
        elif opcao == "nu":
            novo_cliente(clientes)

        elif opcao == "lu":
            listar_clientes(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()