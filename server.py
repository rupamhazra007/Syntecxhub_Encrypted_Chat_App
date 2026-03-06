import socket
import threading
from encryption import decrypt_message, encrypt_message, load_key
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

key = load_key()

clients = []

def log_message(msg):
    with open("chat_log.txt", "a") as f:
        f.write(msg + "\n")

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(client_socket)

    while True:
        try:
            encrypted_msg = client_socket.recv(4096)
            if not encrypted_msg:
                break

            decrypted = decrypt_message(encrypted_msg, key)

            timestamp = datetime.now().strftime("%H:%M:%S")
            log = f"[{timestamp}] {addr}: {decrypted}"
            print(log)

            log_message(log)

            encrypted_forward = encrypt_message(log, key)
            broadcast(encrypted_forward, client_socket)

        except:
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"[DISCONNECTED] {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

start_server()