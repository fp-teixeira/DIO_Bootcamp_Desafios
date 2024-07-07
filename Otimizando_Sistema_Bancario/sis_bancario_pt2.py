'''
Proposta de solução de desafio "Otimizando o Sistema Bancário com Funções Python". Esta solução usa 
como base a resposta do desafio anterior, com as implementações solicitadas pelo instrutor.

Como as funções de saque, deposito e extrato foram realizadas no desafio anterior, foram implementadas
nesta segunda parte apenas as funções de cadastrar usuário e criar conta, além das alterações solicitadas
pelo instrutor para as funções anteriores, para treinamento de conceitos.

Função cpf_valido para fazer validação dos CPFs cadastrados.
Funções para listar usuários e contas.

Funções Deposito, Saque e Extrato ainda não atribuidas a usuários.

Validação de outros argumentos para implementações futuras.

'''

class ContaBanco:
    def __init__(self):
        self.saldo = 0
        self.numero_saques = 0
        self.extrato = ""
        self.usuarios= dict()
        self.addconta= dict()
        self.proxima_conta = 1
        

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.adicionar_extrato('Depósito', valor)
            print(f'Depósito de R${valor:.2f} efetuado com sucesso.')
            return self.saldo
        else:
            print('O valor do depósito deve ser positivo.')
            return self.saldo

    def sacar(self, valor, limite,LIMITE_SAQUES):
        if valor <= 0:
            print('O valor de saque deve ser positivo.')
            return self.saldo
        if valor > limite:
            print('Saque inválido. Valor acima do limite disponível.')
            return self.saldo
        if self.numero_saques >= LIMITE_SAQUES:
            print('Saque inválido. Número máximo de saques atingido.')
            return self.saldo
        if valor > self.saldo:
            print('Saque inválido. Saldo insuficiente.')
            return self.saldo

        self.saldo -= valor
        self.adicionar_extrato('Saque', valor)
        self.numero_saques += 1
        print(f'Saque de R${valor:.2f} efetuado com sucesso.')
        print(f'número de saques disponíveis: {LIMITE_SAQUES - self.numero_saques}')      
        return self.saldo


    def adicionar_extrato(self, operacao, valor):
        self.extrato += f"{operacao}: R$ {valor:.2f}\n"

    def saldo_extrato(self, saldo, extrato=None):
        if not extrato:
            print('-------------------------------')
            print("Não há operações recentes.")
        else:
            print('-------------------------------')
            print("Histórico de operações")
            print(extrato)
        print('-------------------------------')
        print(f"\nSaldo: R$ {saldo:.2f}")
        print('-------------------------------')
    
    def criar_conta(self, cpf):
        agencia = "0001"
        usuario = self.usuarios.get(cpf)
        if not usuario:
            print("CPF não encontrado.")
            return None
       
        nome = usuario['nome']
        numero_conta = self.proxima_conta
        self.proxima_conta += 1
       
        self.addconta[numero_conta] = {
           'Agencia': agencia,
           'Titular': nome,
           'Nº Conta': numero_conta

       }
       
        return numero_conta
            
    def cadastrar_usuario(self, nome, data, cpf,endereco):
        
        self.usuarios[cpf] = {'nome': nome,'data_nascimento': data, 'cpf': cpf, 'endereco': endereco }   
        return self.usuarios
    
    def cpf_valido(self):
        while True:
            cpf = input("Informe o CPF do usuário a ser cadastrado (apenas números): ")
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                print("CPF inválido. Deve conter exatamente 11 dígitos.")
                continue
            if cpf in self.usuarios:
                print("CPF já cadastrado. Informe outro CPF.")
                continue
            return cpf
        
    def listar_usuarios(self):  
        if self.usuarios:
            print("Informações dos usuários cadastrados:")
            for cpf, dados in self.usuarios.items():
                print("----------------------------------------")
                print(f"Nome: {dados['nome']}")
                print(f"Data de Nascimento: {dados['data_nascimento']}")
                print(f"CPF: {dados['cpf']}")
                print(f"Endereço: {dados['endereco']}")
                print("----------------------------------------")
        else:
            print("Sem usuários cadastrados.")
            
    def listar_contas(self):
        if self.addconta:
            for numero_conta, dados in self.addconta.items():
                print("----------------------------------------")
                print(f"Agencia: {dados['Agencia']}")
                print(f"Titular: {dados['Titular']}")
                print(f"Nº Conta: {dados['Nº Conta']}")
                print("----------------------------------------")
            
        else:
            print("Sem contas cadastradas.")

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar usuário
[a] Criar conta
[l] Listar usuários cadastrados
[k] Listar contas cadastradas
[q] Sair

=> """

conta = ContaBanco()

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a depositar: "))
        saldo=conta.depositar(valor)
        print(f"\nSaldo: R$ {saldo:.2f}")
    elif opcao == "s":
        valor = float(input("Informe o valor a sacar: "))
        saldo = conta.sacar(valor=valor,limite=500,LIMITE_SAQUES=3)
        if saldo is not None:
            print(f"\nSaldo: R$ {saldo:.2f}")
        else:
            print("A operação de saque falhou. Por favor, tente novamente.")
            
    elif opcao == "e":
        saldo = conta.saldo
        extrato = conta.extrato
        conta.saldo_extrato(saldo, extrato=extrato)
    
    elif opcao == "u":
        nome = input("Informe o nome do usuário a ser cadastrado: ")
        data = input("Informe a data de nascimento (Formato dd/mm/aaaa): ")
        cpf = conta.cpf_valido()
        endereco = input("Informe o endereço (Formato: Logradouro/numero - Bairro - Cidade/Sigla):") 
        novo_usuario = conta.cadastrar_usuario(nome, data, cpf, endereco)

        print("Usuário Criado Com sucesso!") 
        
    elif opcao == "a":
        cpf = input("Informe o cpf do usuário: ")
        cliente_novo = conta.criar_conta(cpf)
        if cliente_novo is not None:
            print("Conta criada com sucesso!")
    
    elif opcao =="l":
        conta.listar_usuarios()
        
    elif opcao =="k":
        conta.listar_contas()
            
    elif opcao == "q":
        break
    else:
        print("Operação inválida, favor selecionar uma opção.")
