'''
Proposta de solução de desafio "Modelando o Sistema Bancário em POO com Python". Esta solução usa 
como base a resposta do desafio anterior, com as implementações solicitadas pelo instrutor e a imagem 
de referência do sistema proposta pelo instrutor.

Validações de cpf e outras entradas foram removidas para uma melhor implementação no futuro 
e simplificação da resposta.

Nomes das classes alteradas de acordo com o esquemático do instrutor.

'''

from abc import ABC, abstractmethod

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
    
    def __str__(self):
        historico_str = "\n".join(map(str, self._transacoes))
        return f"Histórico de transações:\n{historico_str}" if self._transacoes else "Não há operações recentes."

class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta):
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}: R$ {self.valor:.2f}"

class Saque(Transacao):
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Conta:
    _contas = {}

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        Conta._contas[numero] = self

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print('O valor de saque deve ser positivo.')
            return False
        if valor > self._saldo:
            print('Saque inválido. Saldo insuficiente.')
            return False
        self._saldo -= valor
        print('-------------------------------')
        print(f"Saldo: R$ {self.saldo:.2f}")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print('O valor de depósito deve ser positivo.')
            return False
        self._saldo += valor
        print('-------------------------------')
        print(f"Saldo: R$ {self.saldo:.2f}")
        return True

    def exibir_historico(self):
        print('-------------------------------')
        print(self.historico)
        print('-------------------------------')
        print(f"Saldo: R$ {self.saldo:.2f}")

    @classmethod
    def listar_contas(cls):
        if not cls._contas:
            print("Sem contas cadastradas.")
            return
        for numero, conta in cls._contas.items():
            print(f"Número da Conta: {conta.numero}, Agência: {conta._agencia}, Titular: {conta.cliente.nome}")

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saques):
        super().__init__(numero, cliente)
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        if self._numero_saques >= self._limite_saques:
            print('Saque inválido. Número máximo de saques atingido.')
            return False
        if super().sacar(valor):
            self._numero_saques += 1
            return True
        return False

class Cliente:
    _clientes = {}

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    @classmethod
    def nova_conta(cls, cliente, numero_conta, limite_saques=3):
        return ContaCorrente(numero_conta, cliente, limite_saques)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        PessoaFisica._clientes[cpf] = self

    @classmethod
    def cadastrar_usuario(cls, nome, data_nascimento, cpf, endereco):
        if cpf in cls._clientes:
            print("CPF já cadastrado. Informe outro CPF.")
            return None
        cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        print("Usuário criado com sucesso!")
        return cliente

def main():
    while True:
        menu = """      
[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar usuário
[a] Criar conta
[k] Listar contas cadastradas
[q] Sair
        
=> """
        opcao = input(menu).strip().lower()
        
        if opcao == "d":
            numero = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor a depositar: "))
            conta = Conta._contas.get(numero)
            if conta:
                cliente = PessoaFisica._clientes[conta.cliente.cpf]
                cliente.realizar_transacao(conta, Deposito(valor))
            else:
                print("Conta não encontrada.")
        
        elif opcao == "s":
            numero = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor a sacar: "))
            conta = Conta._contas.get(numero)
            if conta:
                cliente = PessoaFisica._clientes[conta.cliente.cpf]
                cliente.realizar_transacao(conta, Saque(valor))
            else:
                print("Conta não encontrada.")

        elif opcao == "e":
            numero = int(input("Informe o número da conta: "))
            conta = Conta._contas.get(numero)
            if conta:
                conta.exibir_historico()
            else:
                print("Conta não encontrada.")
        
        elif opcao == "u":
            nome = input("Informe o nome do usuário a ser cadastrado: ")
            data = input("Informe a data de nascimento (Formato dd/mm/aaaa): ")
            cpf = input("Informe o CPF do usuário (apenas números): ").strip()
            endereco = input("Informe o endereço (Formato: Logradouro/numero - Bairro - Cidade/Sigla):")
            PessoaFisica.cadastrar_usuario(nome, data, cpf, endereco)
        
        elif opcao == "a":
            cpf = input("Informe o CPF do usuário: ").strip()
            cliente = PessoaFisica._clientes.get(cpf)
            if cliente:
                numero_conta = len(Conta._contas) + 1
                conta = Cliente.nova_conta(cliente, numero_conta)
                cliente.adicionar_conta(conta)
                print("Conta criada com sucesso!")
            else:
                print("CPF não encontrado.")

        elif opcao == "k":
            Conta.listar_contas()
        
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, favor selecionar uma opção.")

if __name__ == "__main__":
    main()
