import socket
import sys
import asyncio
import aioconsole # type: ignore

host = '10.10.10.11'
port = 13337

async def send_message(writer):
    message = await aioconsole.ainput("Chat : ")
    writer.write(message.encode('utf-8'))
    await writer.drain()

async def receive_message(reader):
    while True:
        data = await reader.read(1024)
        if not data:
            print("Le serveur a fermé la connexion.")
            break
        print(f"Le serveur a répondu : {repr(data.decode('utf-8'))}")

async def main():
    while True:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            print(f"Connecté avec succès au serveur {host} sur le port {port}")

            await asyncio.gather(send_message(writer), receive_message(reader))

        except Exception as e:
            print(f"Erreur de connexion : {e}. Réessai en 5 secondes...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())