import socket
import threading

host = '10.10.10.11'
port = 13337

clients = []  # Liste pour stocker les connexions des clients

# Fonction pour gérer chaque client
def handle_client(conn, addr):
    print(f"Connexion établie avec {addr[0]}:{addr[1]}")
    pseudo = conn.recv(1024).decode('utf-8')  # On suppose que le client envoie son pseudo en premier
    broadcast(f"{pseudo} a rejoint le chat!".encode('utf-8'), conn)

    while True:
        try:
            message = conn.recv(1024)
            if message:
                broadcast(message, conn, pseudo)
            else:
                remove_client(conn)
                break
        except:
            remove_client(conn)
            break

# Diffuser un message à tous les clients sauf l'envoyeur
def broadcast(message, connection, pseudo=""):
    for client in clients:
        if client != connection:
            try:
                client.send(f"{pseudo}: ".encode('utf-8') + message)
            except:
                remove_client(client)

# Supprimer un client de la liste des clients
def remove_client(connection):
    if connection in clients:
        clients.remove(connection)

# Démarrage du serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"Le serveur est prêt et écoute sur {host}:{port}")

        while True:
            conn, addr = server.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        print(f"Erreur serveur : {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
