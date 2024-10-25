import socket
import sys
import asyncio

host = '10.10.10.11'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")

    message = input("Que veux-tu envoyer au serveur : ")

    s.sendall(message.encode('utf-8'))

    data = s.recv(1024)

    print(f"Le serveur a répondu : {repr(data)}")

except Exception as e:
    print(f"Erreur lors de la connexion au serveur : {e}")

finally:
    s.close()
    sys.exit(0)
