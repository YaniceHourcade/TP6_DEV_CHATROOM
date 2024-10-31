import asyncio
import datetime
import os
import logging

CLIENTS = {}

HOST = "10.10.10.11"
PORT = 13337

specific_path = r"/var/log/chat_serveur"
LOG_FILE = os.path.join(specific_path, "chat_serveur.log")

# Création du répertoire spécifique si nécessaire
try:
    os.makedirs(specific_path, exist_ok=True)
    print(f"Le répertoire '{specific_path}' est prêt.")
except PermissionError:
    print(f"Permission refusée : Impossible de créer '{specific_path}'.")
    exit(1)
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    exit(1)

# Création du fichier de log
try:
    with open(LOG_FILE, 'a'):
        pass
    print(f"Le fichier de log '{LOG_FILE}' est prêt.")
except PermissionError:
    print(f"Permission refusée : Impossible de créer '{LOG_FILE}'.")
    exit(1)
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    exit(1)

# Configuration du logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    logging.info(f"Un client vient de se connecter avec l'IP {addr[0]} et le port {addr[1]}")
    print(f"Un client vient de se connecter avec l'IP {addr[0]} et le port {addr[1]}")

    # Stocker le client dans CLIENTS
    CLIENTS[addr] = {"r": reader, "w": writer, "pseudo": None}

    try:
        data = await reader.read(1024)
        message = data.decode("utf-8")

        if message.startswith("Hello|"):
            pseudo = message.split("|")[1]  # Isoler le pseud
            CLIENTS[addr]["pseudo"] = pseudo  # Stocker le pseudo
            time = datetime.datetime.now().strftime("%H:%M")
            print(f"{pseudo} a rejoint la room à {time}")
            logging.info(f"{pseudo} a rejoint la room")

            # Annonce à tous les autres clients
            for client_addr, client in CLIENTS.items():
                if (
                    client_addr != addr
                ):  # Ne pas envoyer au client qui vient de se connecter
                    response = f"Annonce : {pseudo} a rejoint la chatroom à {time}\n"
                    client["w"].write(response.encode("utf-8"))
                    await client["w"].drain()

        while True:
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode("utf-8")
            print(f"{pseudo} a dit : {message}")
            logging.info(f"{pseudo} a dit : {message}")

            # Envoi du message à tous les autres clients
            for client_addr, client in CLIENTS.items():
                pseudo = CLIENTS[addr]["pseudo"]
                time = datetime.datetime.now().strftime("%H:%M")
                if client_addr != addr:  # Ne pas envoyer au client qui a envoyé le message
                    response = f"{time} {pseudo} a dit : {message}\n"  # Utiliser le pseudo dans la réponse
                    client["w"].write(response.encode("utf-8"))
                    await client["w"].drain()

    finally:
        pseudo = CLIENTS[addr]["pseudo"]
        print(f"Connexion fermée pour {pseudo}")
        logging.info(f"Connexion fermée pour {pseudo}")
        

        del CLIENTS[addr]

        # Informer les autres clients de la déconnexion
        if pseudo:
            for client_addr, client in CLIENTS.items():
                response = f"Annonce : {pseudo} a quitté la chatroom\n"
                client["w"].write(response.encode("utf-8"))
                await client["w"].drain()

        writer.close()  # Ferme la connexion


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    logging.info(f"Serveur démarré sur {HOST}:{PORT}")
    print(f"Serveur en cours d'exécution sur {addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()  # Maintient le serveur en cours d'exécution


if __name__ == "__main__":
    asyncio.run(main())
