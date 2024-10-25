import sys
import requests

# Fonction pour récupérer le contenu de la page web
def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text  
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL : {e}")
        sys.exit(1)

# Fonction pour écrire le contenu dans un fichier
def write_content(content, file):
    try:
        # Ouvre le fichier en mode écriture (écrasera le fichier s'il existe déjà)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Contenu écrit dans {file}")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")
        sys.exit(1)

# Fonction principale pour gérer l'argument d'URL et lancer les fonctions
def main():
    if len(sys.argv) != 2:
        print("Usage : python web_sync.py <URL>")
        sys.exit(1)

    url = sys.argv[1]  # Récupère l'URL passée en argument

    print(f"Téléchargement du contenu de la page : {url}")

    # Télécharge le contenu de la page
    content = get_content(url)

    # Définir le chemin du fichier de destination
    file_path = "/tmp/web_page"

    # Écrire le contenu dans le fichier
    write_content(content, file_path)

if __name__ == "__main__":
    main()
