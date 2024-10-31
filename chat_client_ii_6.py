from csv import writer
import datetime
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
    try :
        while True:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            input = await aioconsole.ainput("Chat : ")
            message = input + time
            writer.write(message.encode("utf-8"))
            await writer.drain()
    except asyncio.CancelledError:
        pass


async def receive_message(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("Le serveur a fermé la connexion.")
                break
            print(f"\nChat recu : {repr(data.decode('utf-8'))}")
    except asyncio.CancelledError:
        pass
    finally:
        print("Fermeture de la connexion...")
        writer.close()
        await writer.wait_closed()
        print("Connexion fermée. Au revoir!")


async def main():
    while True:
        try:
            reader, writer = await asyncio.open_connection(HOST, PORT)
            print(f"Connecté avec succès au serveur {HOST} sur le port {PORT}")

            await send_pseudo(writer)
            # Exécutez l'envoi et la réception en parallèle
            send_task = asyncio.create_task(send_message(writer))
            receive_task = asyncio.create_task(receive_message(reader, writer))

            send_task.cancel()
            receive_task.cancel()
            await asyncio.gather(send_task, receive_task, return_exceptions=True)
            break  # Exit the loop on disconnection
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgramme interrompu.")
