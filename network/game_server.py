import socket
import threading

class GameServer:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print("Server started and listening on port", port)
        self.clients = []

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
                    response = f"Server received: {message}"
                    client_socket.send(response.encode('utf-8'))
                else:
                    break
            except ConnectionResetError:
                break
        client_socket.close()
        self.clients.remove(client_socket)

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()
