import threading
import socket
import constant

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((constant.CHAT_SERVER_IP, constant.CHAT_SERVER_PORT))


def client_receive():
    while True:
        try:
            message = client.recv(constant.CLIENT_RECV_PORT).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
