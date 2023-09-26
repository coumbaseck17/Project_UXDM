import os

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

# def fetch_genre_song(url):
#
#     endpoint = "/search/genre"
#
#
#     with open("data/popularity.json", "r", encoding="utf-8") as json_file:
#         genre_data_list = json.load(json_file)
#
#     for genre_data in genre_data_list:
#
#         json_file_id = genre_data["_id"]
#         params = {"genreName": json_file_id}
#         data = api_request(url, endpoint, params)
#         """if response and response.status_code == 200:
#             genre_data_list = response.json()
#             # Maintenant, vous pouvez utiliser genre_data_list
#         else:
#             print("La requête a échoué avec le code de statut :", response.status_code)"""
#
#         return genre_data







