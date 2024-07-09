import socket
import threading
HOST = '127.0.0.1'
PORT = 1489
LIMIT = 10
active_clients = []

def listen_from_message(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = f"{username}~{message}"
                sending_message_to_all(final_msg)
            else:
                break
        except:
            break

def send_message_to_client(client, message):
    client.sendall(message.encode())

def sending_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    username = client.recv(2048).decode('utf-8')
    if username:
        active_clients.append((username, client))
        prompt_message = f"CHATBOT ~ {username} joined the chat"
        sending_message_to_all(prompt_message)
    threading.Thread(target=listen_from_message, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(LIMIT)
    print(f"Server running on {HOST}:{PORT}")

    while True:
        client, _ = server.accept()
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
