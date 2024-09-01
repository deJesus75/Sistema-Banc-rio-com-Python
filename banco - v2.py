###Simulação de um Sistema Bancario
###criado por Wilian Oliveira de Jesus
###27 de agosto de 2024
###########################################
## versão 2  31/08/2024
## Adicionadas as funçoes :criar_usuario() e criar conta()
## Padronizadas as entradas e saidas das funçoes conforme o
## desafio 2
############################################

###Variaveis de entrada
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

saldo = 0
limite = 500
extrato = ""
numero_operacoes = 0
LIMITE_OPERACOES = 10
AGENCIA = '0001'


conta = {'agencia':'','numero':0,'usuario_cpf':''}

usuarios = {}
contas = {}
ultima_conta=0

############################# mensagens de ERROS ###############################################
erros={'valor':'Operação falhou! O valor informado é invalido. ',
       'saldo':'Operação falhou! Você não tem saldo suficiente.',
       'limite':'Operação falhou! O valor do saque excede o limite de R$ 500.00 por saque.',
       'numero_operacoes':'Operação falhou! Número máximo de operações diárias excedido.',
       'operacao':'Operação inválida , Por favor selecione novamente a operação desejada.'}

############################## funçoes ####################################################
def deposito(valor,saldo,extrato,/):#argumento posicional
    saldo += valor
    extrato += f'Deposito : R$ {valor:.2f}\n'
    return saldo,extrato
    
def saque(*,v=0,s=0,e=''):#argumento nomeado
    s -= v
    e += f'   Saque : R$ {valor:.2f}\n'
    return s,e

def add_extrato(op,valor):
    linha_estrato = f'{opcoes[op]}: R$ {valor:.2f}\n'
    return linha_estrato

def exibi_extrato(saldo,/,*,extrato):
    print('\n ======================= EXTRATO ========================')
    print('Não foram realizados movimentos.' if not extrato else extrato)
    print(f'\n Saldo :R$ {saldo:.2f}')
    print('\n ========================================================')


def criar_usuario(usuarios):
    cpf = input('Digite o CPF:')
    if cpf not in usuarios: 
        usuario = dict.fromkeys([cpf])
        usuario[cpf]= dict.fromkeys(['nome','data','endereco'])
        usuario[cpf]['nome'] = input('Digite o  nome:')
        usuario[cpf]['data'] = input('Digite a data de nascimento:')
        usuario[cpf]['endereco']= dict.fromkeys(['lougradouro','num','bairro','cidade_estado'])
        usuario[cpf]['endereco'] ['lougradouro']= input('Digite a rua:')
        usuario[cpf]['endereco'] ['num']= input('Digite o numero:')
        usuario[cpf]['endereco'] ['bairro']= input('Digite o bairro:')
        usuario[cpf]['endereco'] ['cidade_estado']= input('Digite a cidade/sigla estado:')
        return usuario
    else:
        print('Falha no cadastro! Usuario/CPF já cadastrado')
        return False

def lista_usuarios(usuarios):
    if usuarios:
     for chave,valor in usuarios.items():
        print('******************************************************')
        print(f'    CPF  : {chave}')
        print(f'    Nome : {usuarios[chave]['nome']}')
        print(f'Endereço : {usuarios[chave]['endereco']['cidade_estado']}')
        print('******************************************************')
        print()
     return
    else:
        print("Não tem usuarios cadastrados!")

def criar_conta(ultima_conta):
    cpf = input('Digite o CPF:')
    if cpf not in usuarios:
        print('Falha no cadastro! Usuario/CPF não tem cadastrado')
        return False,False
    else:
        ultima_conta += 1
        conta = dict.fromkeys([ultima_conta])
        conta[ultima_conta] = dict.fromkeys(['agencia','usuario_cpf'])
        conta[ultima_conta]['agencia'] = AGENCIA
        conta[ultima_conta]['usuario_cpf'] = cpf
        return conta,ultima_conta

def lista_contas(contas, usuarios):
    if contas:
         for chave,valor in contas.items():
            print('******************************************************')
            print(f'Número da conta : {chave}')
            print(f'        Agencia : {contas[chave]['agencia']}')
            print(f'            CPF : {contas[chave]['usuario_cpf']}')
            print(f'           Nome : {usuarios[contas[chave]['usuario_cpf']]['nome']}')
            print('******************************************************')
            print()
         return
    else:
        print("Não tem contas cadastrados!")
        return False
        

################################################################################################

while True:

    opcao = input(menu)
############################ opcao 1  Deposito ############################
    if opcao == '1':
        valor = float(input ('Informe o valor do deposito: '))
        excedeu_operacoes= numero_operacoes >= LIMITE_OPERACOES
        
        if excedeu_operacoes:
            print(erros['numero_operacoes'])
        elif valor > 0:
            entrada = deposito(valor,saldo,extrato)
            extrato= entrada[1]
            saldo = entrada[0]
            numero_operacoes += 1

        else:
            print(erros['valor'])
            
############################ opcao 2 Saque ############################            
    elif opcao == '2':

        valor = float( input('Informe o valor do saque: '))
        excedeu_saldo = valor >saldo
        excedeu_limite= valor > limite
        excedeu_operacoes= numero_operacoes >= LIMITE_OPERACOES

        if excedeu_saldo:
            print(erros['saldo'])

        elif excedeu_limite:
            print(erros['limite'])

        elif excedeu_operacoes:
            print(erros['numero_operacoes'])

        elif valor>0:
            saida = saque(v=valor,s=saldo,e=extrato)
            extrato= saida[1]
            saldo = saida[0]
            numero_operacoes += 1

        else:
            print(erros['valor'])

        
############################ opcao 3 Extrato ############################        
    elif opcao == '3':
        exibi_extrato(saldo,extrato=extrato)
        
############################ opcao 4  ######################################### 

    elif opcao == '4':
         usuario = criar_usuario(usuarios)
         if usuario:
            usuarios.update(usuario)
            
############################ opcao 5 Lista Usuarios ############################ 
    elif opcao == '5':
        lista_usuarios(usuarios)

############################ opcao 6 Cria contas ############################### 
        
    elif opcao == '6':
         conta = criar_conta(ultima_conta)
         if conta[0]:
            contas.update(conta[0])
            ultima_conta=conta[1]
############################ opcao 7 Lista contas ############################ 

    elif opcao == '7':
            lista_contas(contas, usuarios)
            
        
############################ opcao q Sair ############################
    elif opcao == 'q':
        break

########################### opcao invalida ###########################
    else:
        print(erros['valor'])
    

        
        
