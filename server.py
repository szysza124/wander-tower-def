import threading 
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message.decode('utf-8'))
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'[SERWER] Gracz {nickname} opuścił grę.'.encode('utf-8'))
                nicknames.remove(nickname)
            break

def receive():
    print("Serwer gry uruchomiony! Oczekiwanie na graczy...")
    while True:
        client, address = server.accept()
        print(f"Połączono z adresem {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Dołączył gracz o nicku: {nickname}')
        broadcast(f'[SERWER] {nickname} dołączył do rozgrywki!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()