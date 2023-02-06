import socket
from threading import *


def getSaldo():
    try:
        client.send("getSaldo".encode())
        resultado = client.recv(1024).decode()
        print("este é seu saldo: "+resultado)
    except:
        print('ocorreu um erro durante a operação')
        client.close()


def deposito():
    try:
        client.send("deposito".encode())
    except:
        print('ocorreu um erro de comunicação com o servidor')
        client.close()
    while(True):
        try:
            valor = float(input('informe o valor que você deseja depositar: '))
            #arredonda o valor para 2 casas decimais
            valor = round(valor, 2)
            if (valor <= 0):
                print("o valor não pode ser 0 ou negativo!")
                raise Exception()
        except:
            print('error: informe um valor aceitavel!')
        else:
            break
    try:
        client.send(str(valor).encode())
        novoSaldo = client.recv(1024).decode()
        print("este é seu saldo: "+novoSaldo)
    except:
        print('ocorreu um erro durante a operação')
        client.close()


def saque():
    try:
        client.send("saque".encode())
    except:
        print('ocorreu um erro de comunicação com o servidor')
        client.close()
    while(True):
        try:
            valor = float(input('informe o valor que você deseja sacar: '))
            #arredonda o valor para 2 casas decimais
            valor = round(valor, 2)
            if (valor <= 0):
                print("o valor não pode ser 0 ou negativo!")
                raise Exception()
        except:
            print('error: informe um valor aceitavel!')
        else:
            break
    try:
        client.send(str(valor).encode())
        novoSaldo = client.recv(1024).decode()
        if(novoSaldo=="error"):
            print('você não tem saldo suficiente para este saque')
            raise Exception()
        print("este é seu saldo: "+novoSaldo)
    except:
        print('ocorreu um erro durante a operação')
        client.close()
    


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao = True
try:
    client.connect(('localhost', 7777))
except ConnectionRefusedError:
    print('a conexão foi recusada. Nenhuma porta aceitou a requesição')
    conexao = False

if conexao:
    print('Cliente conectado.\n')
    while True:
        print('informe qual operação você deseja fazer:')
        o = input('digite 1 para ver saldo, 2 para fazer deposito, 3 para fazer saque e qualquer outra coisa para sair: ')
        if o == '1':
            getSaldo()
        elif o == '2':
            deposito()
        elif o == '3':
            saque()
        else:
            print('operação encerrada')
            client.close()
            break
else:
    print('Operação encerrada: Ocorreu um erro na conexão!')
print('conexão encerrada')
