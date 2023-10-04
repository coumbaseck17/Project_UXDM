import os
import urllib

import requests
import json

url = "https://wasabi.i3s.unice.fr"

params = {}

def api_request(url, endpoint, params) :
    """Effectue une requête GET à l'API avec les paramètres spécifiés."""
    try:
        response = requests.get(url + endpoint, params)

        if response.status_code == 200:
            return response.json()
        else:
            print("La requête a échoué avec le code de statut :", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête :", e)
        return None

# recuperer les genres plus populaires
def fetch_genre_popularity(url):

    endpoint = "/api/v1/artist/genres/popularity"
    params = { "limit" : "10"}

    popularity_data = api_request(url, endpoint, params)

    if popularity_data:
        # si le fichier existe
        if not os.path.exists("popularity.json"):
            # S'il n'existe pas
            with open("data/popularity.json", "w", encoding="utf-8") as json_file:
                json.dump(popularity_data, json_file, ensure_ascii=False, indent=4)
        else:
            print("Le fichier 'artist_popularity.json' existe déjà. Les données ne seront pas écrasées.")

    return popularity_data


# Fonction pour récupérer les artistes en fonction d'un genre depuis l'API Wasabi
def fetch_artists_by_genre( genre):
    endpoint = f"/search/genre/{genre}"
    params = {}

    try:
        response = requests.get(url + endpoint, params)
        if response.status_code == 200:
            data = response.json()
            artists = []

            for item in data:
                if "id_artist_deezer" in item:
                    artist_name = item.get("name", "")
                    if artist_name not in artists:
                        artists.append(artist_name)

            return artists

        else:
            print(f"La requête a échoué avec le code de statut : {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête :", e)
        return None

