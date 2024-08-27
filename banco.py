###Simulação de um Sistema Bancario
###criado por Wilian Oliveira de Jesus
###27 de agosto de 2024

###Variaveis de entrada
menu = '''
Selecione uma opção:

*********************
       Menu
*********************

[1] Depositar
[2] Sacar
[3] Extrato
[q] Sair

=> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
opcoes = {'1':'Deposito','2':'Saque'}

############################# mensagens de ERROS ###############################################
erros={'valor':'Operação falhou! O valor informado é invalido. ',
       'saldo':'Operação falhou! Você não tem saldo suficiente.',
       'limite':'Operação falhou! O valor do saque excede o limite de R$ 500.00 por saque.',
       'numero_saques':'Operação falhou! Número máximo de saques diários excedido.',
       'operacao':'Operação inválida , Por favor selecione novamente a operação desejada.'}

############################## funçoes ####################################################
def deposito(valor):
    global saldo
    saldo += valor
    
def saque(valor):
    global saldo
    saldo -= valor

def add_extrato(op,valor):
    linha_estrato = f'{opcoes[op]}: R$ {valor:.2f}\n'
    return linha_estrato

def exibi_extrato(extrato):
    print('\n ======================= EXTRATO ========================')
    print('Não foram realizados movimentos.' if not extrato else extrato)
    print(f'\n Saldo :R$ {saldo:.2f}')
    print('\n ========================================================')
    

################################################################################################

while True:

    opcao = input(menu)
############################ opcao 1  Deposito ############################
    if opcao == '1':
        valor = float(input ('Informe o valor do deposito: '))

        if valor > 0:
            deposito(valor)
            extrato += add_extrato(opcao,valor)

        else:
            print(erros['valor'])
            
############################ opcao 2 Saque ############################            
    elif opcao == '2':

        valor = float( input('Informe o valor do saque: '))
        excedeu_saldo = valor >saldo
        excedeu_limite= valor > limite
        excedeu_saques= numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print(erros['saldo'])

        elif excedeu_limite:
            print(erros['limite'])

        elif excedeu_saques:
            print(erros['numero_saques'])

        elif valor>0:
            saque(valor)
            extrato += add_extrato(opcao,valor)
            numero_saques += 1

        else:
            print(erros['valor'])

        
############################ opcao 3 Extrato ############################        
    elif opcao == '3':
        exibi_extrato(extrato)
        
############################ opcao q Sair ############################
    elif opcao == 'q':
        break

########################### opcao invalida ###########################
    else:
        print(erros['valor'])
    

        
        
