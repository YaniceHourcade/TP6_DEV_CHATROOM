import asyncio

host = '10.10.10.11' 
port = 13337 

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Un client vient de se connecter avec l'IP {addr[0]} et le port {addr[1]}")

    while True:
        data = await reader.read(1024)
        if not data:
            break 

        message = data.decode('utf-8')
        print(f"Données reçues du client : {message}")

        response = f"Hello {addr[0]}:{addr[1]}"
        writer.write(response.encode('utf-8'))  # Envoie la réponse au client
        await writer.drain()  # Assure que les données sont envoyées

    print(f"Connexion fermée pour {addr}")
    writer.close()  # Ferme la connexion

async def main():
    server = await asyncio.start_server(handle_client, host, port)

    addr = server.sockets[0].getsockname()
    print(f'Serveur en cours d\'exécution sur {addr[0]}:{addr[1]}')

    async with server:
        await server.serve_forever()  # Maintient le serveur en cours d'exécution

if __name__ == '__main__':
    asyncio.run(main()) 


