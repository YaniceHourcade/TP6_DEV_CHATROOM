import sys
import requests
import os

# Fonction pour récupérer le contenu de la page web
def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text  
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL {url}: {e}")
        return None  # Retourne None en cas d'erreur

# Fonction pour écrire le contenu dans un fichier
def write_content(content, file):
    try:
        # Ouvre le fichier en mode écriture
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Contenu écrit dans {file}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier {file}: {e}")

# Fonction principale pour gérer l'argument du chemin de fichier contenant les URLs
def main():
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
        urls = file.readlines()

    # Traiter chaque URL
    for url in urls:
        url = url.strip()  # Supprimer les espaces et les sauts de ligne
        if not url:
            continue

        print(f"Téléchargement du contenu de la page : {url}")

        # Télécharge le contenu de la page
        content = get_content(url)

        # Définir le chemin du fichier de destination
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")  # Remplace les caractères non autorisés
        output_file_path = f"/tmp/web_page"

        # Écrire le contenu dans le fichier s'il a été récupéré avec succès
        if content:
            write_content(content, output_file_path)

if __name__ == "__main__":
    main()
