import socket
import threading
from encryption import encrypt_message, decrypt_message, load_key

HOST = "127.0.0.1"
PORT = 5000

key = load_key()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            encrypted_msg = client.recv(4096)
            if not encrypted_msg:
                break

            message = decrypt_message(encrypted_msg, key)
            print(message)

        except:
            break

def send_messages():
    while True:
        message = input()
        encrypted = encrypt_message(message, key)
        client.send(encrypted)

threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()