from csv import writer
import sys
import asyncio
import aiconsole
import os
import logging

HOST = "10.10.10.11"
PORT = 13337

specific_path = r"/var/log/chat_client"
LOG_FILE = os.path.join(specific_path, "chat_client.log")

# Création du répertoire spécifique si besoin
try:
    os.makedirs(specific_path, exist_ok=True)
    print(f"Le répertoire '{specific_path}' est prêt.")
except PermissionError:
    print(f"Permission refusée : Impossible de créer '{specific_path}'.")
    exit(1)
except Exception as e:
    print(f"Une erreur est survenue : {e}")
    exit(1)

# Vérification de la possibilité de créer le fichier de log
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


async def send_pseudo(writer):
    input = await aioconsole.ainput("Votre Pseudo : ")
    logging.info(f"Pseudo utilisé : {input}")
    message = "Hello|" + input
    writer.write(message.encode("utf-8"))
    await writer.drain()


async def send_message(writer):
    while True:
        message = await aioconsole.ainput("Chat : ")
        logging.info(f"Message envoyer : {message}")
        writer.write(message.encode("utf-8"))
        await writer.drain()


async def receive_message(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Le serveur a fermé la connexion.")
                logging.info(f"Le serveur a fermé la connexion.")
                break
            print(f"\nChat recu : {repr(data.decode('utf-8'))}")
    except Exception as e:
        print(f"Erreur de réception de message : {e}")
        logging.error(f"Erreur de réception de message")
    finally:
        print(f"Fermeture de la connexion...")
        writer.close()
        await writer.wait_closed()
        print(f"Connexion fermée. Au revoir!")
        sys.exit(0)


async def main():
    while True:
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            print(f"Connecté avec succès au serveur {HOST} sur le port {PORT}")
            logging.info(f"Connexion réussie à {HOST}:{PORT}")

            await send_pseudo(writer)
            # Exécutez l'envoi et la réception en parallèle
            await asyncio.gather(send_message(writer), receive_message(reader))

        except Exception as e:
            logging.error(f"Erreur de connexion")
            print(f"Erreur de connexion")
            break


if __name__ == "__main__":
    asyncio.run(main())
