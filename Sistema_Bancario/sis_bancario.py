'''
Proposta de solução de desafio "Criando um Sistema Bancário com Python". Esta solução usa como base o
template disponibilizado pelo instrutor para resolução deste desafio.

Embora não tenha sido necessário, optei pela criação de uma classe para organização das
funçoes de operação (Depósito, Saque e Extrato). A função 'adicionar_extrato' serve apenas para
fins de organização do código, sendo opcional.

'''

class ContaBanco:
    def __init__(self):
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.adicionar_extrato('Depósito', valor)
            print(f'Depósito de R${valor:.2f} efetuado com sucesso.')
            print(f"\nSaldo: R$ {self.saldo:.2f}")
        else:
            print('O valor do depósito deve ser positivo.')

    def sacar(self, valor):
        if valor > self.limite:
            print('Saque inválido. Valor acima do limite disponível.')
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print('Saque inválido. Número máximo de saques atingido.')
        elif valor > self.saldo:
            print('Saque inválido. Saldo insuficiente.')
        elif valor > 0:
            self.saldo -= valor
            self.adicionar_extrato('Saque', valor)
            print(f'Saque de R${valor:.2f} efetuado com sucesso.')
            print(f'número de saques disponíveis: {2 - self.numero_saques}')
            print(f"\nSaldo: R$ {self.saldo:.2f}")
            self.numero_saques += 1
        else:
            print('O valor de saque deve ser positivo.')

    def adicionar_extrato(self, operacao, valor):
        self.extrato += f"{operacao}: R$ {valor:.2f}\n"

    def saldo_extrato(self):
        if not self.extrato:
            print("Não há operações recentes.")
            print(f"\nSaldo: R$ {self.saldo:.2f}")
        else:
            print("Histórico de operações\n")
            print('-------------------------------')
            print(self.extrato)
            print('-------------------------------')
            print(f"\nSaldo: R$ {self.saldo:.2f}")
            print('-------------------------------')

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

conta = ContaBanco()

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a depositar: "))
        conta.depositar(valor)
    elif opcao == "s":
        valor = float(input("Informe o valor a sacar: "))
        conta.sacar(valor)
    elif opcao == "e":
        conta.saldo_extrato()
    elif opcao == "q":
        break
    else:
        print("Operação inválida, favor selecionar uma opção.")
