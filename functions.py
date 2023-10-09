import os
import urllib

import requests
import json

url = "https://wasabi.i3s.unice.fr"

params = {}

"""Effectue une requête GET à l'API avec les paramètres spécifiés."""
def api_request(url, endpoint, params) :
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


"""recuperer les genres plus populaires"""
def fetch_genre_popularity(url):

    endpoint = "/api/v1/artist/genres/popularity"


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




"""Fonction pour récupérer les noms des artistes en fonction d'un genre depuis l'API Wasabi"""
def fetch_artists_by_genre(url):
    endpoint = "/search/genre/"

    with open("data/popularity.json", "r", encoding="utf-8") as json_file:
        genre_data_list = json.load(json_file)

        for genre_data in genre_data_list:
            json_file_id = genre_data["_id"]
            json_file_id_encoded = urllib.parse.quote(json_file_id)

            # Réinitialiser endpoint à chaque boucle
            endpoint = "/search/genre/" + json_file_id_encoded

            data = api_request(url, endpoint, {})

            """debug"""
            # print("genre: " + json_file_id_encoded)
            # print(url, endpoint, {})
            # print(data)

            # Créez un ensemble pour stocker les noms uniques d'artistes
            unique_names = set()

            for entry in data:
                artist_name = entry.get("name")
                if artist_name:
                    unique_names.add(artist_name)

            names_list = list(unique_names)

            # Enregistrer les données dans un fichier JSON (écrasée ou crée)
            file_path = "data/artist_genre/" + json_file_id_encoded + ".json"
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(names_list, json_file, ensure_ascii=False, indent=4)

    return genre_data



def fetch_info_artist(url):

    endpoint = "/search/artist/"

    with open("data/artist_genre/Rock.json", "r", encoding="utf-8") as json_file:
        artist_name_list = json.load(json_file)

        for artist_name in artist_name_list:
            json_file_id_encoded = urllib.parse.quote(artist_name)

            # Réinitialiser endpoint à chaque boucle
            endpoint = "/search/artist/" + json_file_id_encoded

            data = api_request(url, endpoint, {})

            """debug"""
            # print(url, endpoint, {})
            # print(data)

                # Enlevez les caractères interdits dans les noms de fichier
            artist_name_cleaned = artist_name.replace("/", "_")
            file_path = "data/artist_info/rock/" + artist_name_cleaned + ".json"
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

        return artist_name_list






