import requests

def fetch_ts_file(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text  # Retourner le contenu du fichier sous forme de texte
    else:
        raise Exception(
            f"Cannot fetch the file, status code: {response.status_code}")