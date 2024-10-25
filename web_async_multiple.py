import sys
import aiohttp
import asyncio
import os

# Fonction asynchrone pour récupérer le contenu de la page web
async def get_content(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()  
            return await response.text()  
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URL {url}: {e}")
        return None  # Retourne None en cas d'erreur

# Fonction pour écrire le contenu dans un fichier
def write_content(content, file):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Contenu écrit dans {file}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier {file}: {e}")

# Fonction principale pour gérer l'argument du chemin de fichier contenant les URLs
async def main():
    if len(sys.argv) != 2:
        print("Usage : python web_sync.py <chemin_fichier_urls>")
        sys.exit(1)

    file_path = sys.argv[1]  # Récupère le chemin du fichier passé en argument

    # Vérifie si le fichier existe
    if not os.path.isfile(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        sys.exit(1)

    # Lire les URLs depuis le fichier
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]

    # Utilisation d'une session aiohttp pour effectuer des requêtes
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            print(f"Téléchargement du contenu de la page : {url}")
            tasks.append(get_content(session, url))  # Crée une tâche pour chaque URL

        # Attendre que toutes les tâches soient terminées
        contents = await asyncio.gather(*tasks)

        # Écrire le contenu dans des fichiers
        for url, content in zip(urls, contents):
            if content:
                # Définir le chemin du fichier de destination
                filename = url.replace("https://", "").replace("http://", "").replace("/", "_")  # Remplace les caractères non autorisés
                output_file_path = f"/tmp/{filename}.html"  # Assurez-vous que le fichier a l'extension HTML
                write_content(content, output_file_path)

if __name__ == "__main__":
    asyncio.run(main())
