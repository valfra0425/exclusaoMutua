from threading import *
import socket
import time


def getSaldo(connection, address):
    try:
        connection.send(str(saldo).encode())
        print('resultado enviado para o endereço '+str(address))
        operacao(connection, address)
    except:
        print("ocorreu um erro operação cancelada")
        connection.close()


def deposito(connection, address):
    try:
        valor = float(connection.recv(1024).decode())
        time.sleep(5)
        global saldo
        saldo += valor
        connection.send(str(saldo).encode())
        fila.pop(0)
        global ocupado
        ocupado = False
        print('resultado enviado para o endereço '+str(address))
        operacao(connection, address)
    except:
        print("ocorreu um erro operação cancelada")
        connection.close()


def saque(connection, address):
    try:
        valor = float(connection.recv(1024).decode())
        global saldo
        if (valor > saldo):
            connection.send("error".encode())
            operacao(connection, address)
        saldo -= valor
        connection.send(str(saldo).encode())
        fila.pop(0)
        global ocupado
        ocupado = False
        print('resultado enviado para o endereço '+str(address))
        operacao(connection, address)
    except:
        print("ocorreu um erro operação cancelada")
        connection.close()


def operacao(connection, address):
    try:
        o = (connection.recv(1024)).decode()
        if o == "getSaldo":
            getSaldo(connection, address)
        elif o == "deposito":
            coodernador(connection, address, o)
        elif o == "saque":
            coodernador(connection, address, o)
    except:
        print("ocorreu um erro operação cancelada")
        connection.close()


def coodernador(connection, address, o):
    global ocupado
    global fila
    fila.append(address)
    while True:
        if fila[0] == address:
            ocupado = True
            if(o == "deposito"):
                deposito(connection, address)
            elif(o == "saque"):
                saque(connection, address)
            break
        else:
            print('aguarde')
            print(address)
            time.sleep(1)


# o saldo não está sendo armazendado em nenhum lugar então o vaor dele sempre será 1000 ao inicio da execução
saldo = 1000.00
ocupado = False
fila = []
processo_atual = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 7777))
print('Aguardando conexões.\n')
server.listen(2)

while True:

    connection, address = server.accept()
    print(address)

    thread = Thread(target=operacao, args=(connection, address))
    thread.start()
