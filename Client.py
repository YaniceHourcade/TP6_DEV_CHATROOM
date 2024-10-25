import socket
import threading
import sys

host = '10.10.10.11'
port = 13337

# Fonction pour recevoir les messages du serveur
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Erreur lors de la réception des messages.")
            break

# Fonction pour envoyer des messages au serveur
def send_messages(sock):
    while True:
        message = input("")
        try:
            sock.sendall(message.encode('utf-8'))
        except:
            print("Erreur lors de l'envoi du message.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connecté au serveur {host} sur le port {port}")

        pseudo = input("Entrez votre pseudo : ")
        client_socket.sendall(pseudo.encode('utf-8'))

        # Démarrer un thread pour recevoir des messages
        threading.Thread(target=receive_messages, args=(client_socket,)).start()

        # Démarrer un thread pour envoyer des messages
        send_messages(client_socket)

    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
    finally:
        client_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    start_client()
