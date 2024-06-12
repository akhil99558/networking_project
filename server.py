import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[CLIENT]: {message}")
                broadcast(message, client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

# Function to broadcast messages to all clients
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

# Function to remove client from the list
def remove(connection):
    if connection in clients:
        clients.remove(connection)

# Main server code
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []

print(f"Server started at {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Connection established with {client_address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
