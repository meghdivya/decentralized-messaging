import threading
import socket
import constant
from datetime import datetime


class ClientMetadata:
    def __init__(self, address, alias):
        self.address = address
        self.alias = alias
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return 'name={self.alias}, network={self.address}, on {self.date}'.format(self=self)


"""
This handles all client connections and broadcast the client messages
to all other clients
"""

class ChatServer:
    def __init__(self, ip, port):
        self.host = ip
        self.port = port
        self.chatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chatServer.bind((self.host, self.port))
        self.chatServer.listen()
        self.clients = []
        self.aliases = []

    """
    BroadCast the message to all connected clients
    """
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    """
    Gracefully Recieve from client and broadcast the messages
    """
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(constant.CLIENT_RECV_PORT)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                alias = self.aliases[index]
                self.broadcast(
                    f'{alias} has left the chat room!'.encode('utf-8'))
                self.aliases.remove(alias)
                break

    def receive(self):
        while True:
            print('Server is running and listening ...')
            client, address = self.chatServer.accept()

            print(f'connection is established with {str(address)}')
            client.send('alias?'.encode('utf-8'))

            alias = client.recv(constant.CLIENT_RECV_PORT)
            self.aliases.append(alias)
            self.clients.append(client)
            print(f'The alias of this client is {alias}'.encode('utf-8'))

            metadata = ClientMetadata(str(address), alias)
            self.broadcast(
                f'{metadata} has connected to the chat room'.encode('utf-8'))

            client.send('you are now connected!'.encode('utf-8'))
            thread = threading.Thread(
                target=self.handle_client, args=(client,))

            thread.start()


if __name__ == "__main__":
    testChatServer = ChatServer(
        constant.CHAT_SERVER_IP, constant.CHAT_SERVER_PORT)
    testChatServer.receive()
