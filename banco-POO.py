from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime
import textwrap

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    
    def sacar(self,valor):
        saldo = self.saldo
        valor_alto = valor > saldo
        if valor_alto:
            print('Operação Falhou!!! Saldo insuficiente.')
        elif valor > 0:
            self._saldo-=valor
            print('Saque realizado com sucesso')
            return True
        else:
            print('Operação Falhou!!! O valor informado é invalido.')
            
        return False
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print('Deposito realizado')
        else:
            print('Operação Falhou!!! O valor informado é invalido.')
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite=500,limite_saques=3):
        super().__init__(numero,cliente)
        self.limite=limite
        self.limite_saques=limite_saques

    def sacar(self,valor):
        numero_de_saques =len([transacao for transacao in self.historico.transacoes if transacao['tipo']==Saque.__name__])
        passou_do_limite = valor >self.limite
        passou_num_saques = numero_de_saques >= self.limite_saques

        if passou_do_limite:
            print(f'Operação Falhou!!! O limite é de R${self.limite:.2f} por saque')
        elif passou_num_saques:
            print(f'Operação Falhou!!! O número maximode saques é de {self.limite_saques} por dia')
        else:
            return super().sacar(valor)
        
        return False
    def __str__(self):
        return f''' Agência:\t {self.agencia}\n Conta:\t {self.numero} \n Titular:\t{self.cliente.nome}'''
                    

class Transacao (ABC):
    @property
    @abstractproperty
    def valor(self):
        return
    @abstractclassmethod
    def registrar(self,conta):
        return

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas=[]
        
    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self,conta):
        self.contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self,cpf,nome,data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        
    
class Historico:
    def __init__(self):
        self._transacoes=[]
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({'tipo':transacao.__class__.__name__,'valor':transacao.valor,'data':datetime.now().strftime("%d-%m-%Y, %H:%M:%S")})

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor=valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao_ok = conta.depositar(self.valor)
        if transacao_ok:
            conta.historico.adicionar_transacao(self)
        
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao_ok = conta.sacar(self.valor)
        if transacao_ok:
            conta.historico.adicionar_transacao(self)
def le_cpf():
    return input('Informe o CPF :')
def le_valor(operacao):
    return float(input(f'Informe o valor do {operacao}: '))

def verifica_conta(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!!!')
        return
    return cliente.contas[0]

def verifica_cliente(cpf,clientes):
    clientes_existente =[cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_existente[0] if clientes_existente else None

def depositar(clientes):
    cpf = le_cpf()
    cliente = verifica_cliente(cpf,clientes)

    if not cliente:
        print('Cliente não cadastrado!!!!!')
        return
    valor= le_valor('deposito')
    transacao = Deposito(valor)

    conta = verifica_conta(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = le_cpf()
    cliente = verifica_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não cadastrado!!!!!')
        return
    valor= le_valor('saque')
    transacao = Saque(valor)
    conta = verifica_conta(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta,transacao)

def exibir_extrato(clientes):
    cpf = le_cpf()
    cliente = verifica_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não cadastrado!!!!!')
        return
    conta = verifica_conta(cliente)
    if not conta:
        return

    print('===================== Extrato ===================')
    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\t R${transacao['valor']:.2f}'
    print(extrato)
    print(f'\n Saldo:\t R${conta.saldo:.2f}')
    print('=================================================')

def criar_conta(numero_conta,clientes,contas):
    cpf=le_cpf()
    cliente = verifica_cliente(cpf,clientes)
    if not cliente:
        print('Cliente não cadastrado!!!!!')
        return
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta criada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print('-' * 100)
        print(textwrap.dedent(str(conta)))
        print('-' * 100)
def criar_cliente(clientes):
    cpf = le_cpf()
    cliente = verifica_cliente(cpf,clientes)
    if cliente:
        print('Cliente já cadastrado!!!!!')
        return
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Iforme a data de nascimento (dd-mm-aaaa):')
    endereco = input('Informe o endereço (logradouro, numero - bairro -cidade/ estado): ')

    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    clientes.append(cliente)
    print('Cliente cadastrado')

def menu():
    menu = '''
    Selecione uma opção:

    *********************
           Menu
    *********************

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar Usuario
    [5] Lista Usuarios
    [6] Criar Conta
    [7] Lista Contas
    [q] Sair

    => '''
    return input(menu)
    

def main():
    clientes = []
    contas =[]
    while True:
        opcao = menu()
        if opcao == '1':
           depositar(clientes)
            
############################ opcao 2 Saque ############################            
        elif opcao == '2':
            sacar(clientes)

              
############################ opcao 3 Extrato ############################        
        elif opcao == '3':
            exibir_extrato(clientes)
        
        
############################ opcao 4  ######################################### 

        elif opcao == '4':
            criar_cliente(clientes)
        
            
############################ opcao 5 Lista Usuarios ############################ 
        elif opcao == '5':
            print('Em construção')
        

############################ opcao 6 Cria contas ############################### 
        
        elif opcao == '6':
            numero_conta = len(contas)+1
            criar_conta(numero_conta,clientes,contas)
         
############################ opcao 7 Lista contas ############################ 

        elif opcao == '7':
            listar_contas(contas)
        
            
        
############################ opcao q Sair ############################
        elif opcao == 'q':
            break

########################### opcao invalida ###########################
        else:
            print('Opção invalida')
    

    
main()       
