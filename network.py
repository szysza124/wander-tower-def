import threading
import socket
import json

class GameClient:
    def __init__(self, board, nickname="Player1"):
        self.board = board 
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        
        try:
            self.client.connect(('127.0.0.1', 55555))
            self.connected = True
            receive_thread = threading.Thread(target=self.receive, daemon=True)
            receive_thread.start()
        except ConnectionRefusedError:
            print("Serwer offline. Gramy solo.")

    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message.startswith('{'): 
                    try:
                        data = json.loads(message)
                        if data.get('action') == 'next_wave':
                            self.board.start_wave_from_network()
                        elif data.get('nickname') != self.nickname:
                            self.board.network_commands.append(data)
                    except json.JSONDecodeError:
                        pass
                else:
                    print(f"[SIEĆ] {message}") 
            except:
                print("[SIEĆ] Rozłączono z serwerem.")
                self.client.close()
                self.connected = False
                break

    def send_command(self, command_dict):
        if self.connected:
            try:
                command_dict['nickname'] = self.nickname
                message = json.dumps(command_dict)       
                self.client.send(message.encode('utf-8'))
            except:
                pass