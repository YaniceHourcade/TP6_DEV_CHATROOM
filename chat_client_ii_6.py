from csv import writer
import sys
import asyncio
import aioconsole  # type: ignore

HOST = "10.10.10.11"
PORT = 13337


async def send_pseudo(writer):
    input = await aioconsole.ainput("Votre Pseudo : ")
    message = "Hello|" + input
    writer.write(message.encode("utf-8"))
    await writer.drain()


async def send_message(writer):
    while True:
        message = await aioconsole.ainput("Chat : ")
        writer.write(message.encode("utf-8"))
        await writer.drain()


async def receive_message(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("Le serveur a fermé la connexion.")
                
            print(f"\nChat recu : {repr(data.decode('utf-8'))}")
    except Exception as e:
        print(f"Erreur de réception de message : {e}")
    finally:
        print("Fermeture de la connexion...")
        writer.close()
        await writer.wait_closed()
        print("Connexion fermée. Au revoir!")
        sys.exit(0)


async def main():
    while True:
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            print(f"Connecté avec succès au serveur {HOST} sur le port {PORT}")

            await send_pseudo(writer)
            # Exécutez l'envoi et la réception en parallèle
            await asyncio.gather(send_message(writer), receive_message(reader))

        except Exception as e:
            print(f"Erreur de connexion")
            break


if __name__ == "__main__":
    asyncio.run(main())
