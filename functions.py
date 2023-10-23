import os
import urllib
import time
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



# def fetch_info_artist(url):
#
#     endpoint = "/search/artist/"
#     dossier = "data/artist_genre/"
#     list=os.listdir(dossier)
#     for nom_fichier in list:
#         with open("data/artist_genre/"+nom_fichier, "r", encoding="utf-8") as json_file:
#             artist_name_list = json.load(json_file)
#             print(artist_name_list)
#
#
#             for artist_name in artist_name_list:
#                 json_file_id_encoded = urllib.parse.quote(artist_name)
#
#                 # Réinitialiser endpoint à chaque boucle
#                 endpoint = "/search/artist/" + json_file_id_encoded
#
#                 data = api_request(url, endpoint, {})
#
#                 """debug"""
#                 # print(url, endpoint, {})
#                 print(data)
#
#
#                     # Enlevez les caractères interdits dans les noms de fichier
#                 artist_name_cleaned = artist_name.replace("/", "_")
#                 if not os.path.exists("data/artist_info/"+nom_fichier):
#                     os.makedirs("data/artist_info/"+nom_fichier)
#                     file_path = "data/artist_info/"+nom_fichier+"/" + artist_name_cleaned + ".json"
#                     with open(file_path, "w", encoding="utf-8") as json_file:
#                         json.dump(data, json_file, ensure_ascii=False, indent=4)
#
#     return artist_name_list

def fetch_artists_all(url):
    number = 1
    names_genres = []
    number_str= str(number)
    while(number < 77492):
        endpoint = "/api/v1/artist_all/" + number_str
        request = api_request(url, endpoint, {})
        print(endpoint)
        for entry in request:
            artist_deezerFans = entry.get("deezerFans")
            if(artist_deezerFans is not None and artist_deezerFans != 0):

                albums = entry.get("albums")
                members = entry.get("members")
                nombre_albums = len(albums)
                list = []
                list_members = []

                if (members):
                    nombre_members = len(members)
                    for member in members:
                        nom = member["name"]
                        list_members.append(nom)

                # Parcourez la liste des membres et extrayez les noms
                for album in albums:
                    nom = album["title"]
                    list.append(nom)

                data = {
                "id": entry.get("_id"),
                "name": entry.get("name"),
                "type": entry.get("type"),
                "genres": entry.get("genres"),
                "nombre_albums": nombre_albums,
                "nombre_members" : nombre_members,
                "recordLabel": entry.get("recordLabel"),
                "urlDeezer": entry.get("urlDeezer"),
                "gender": entry.get("gender"),
                "picture": entry["picture"]["standard"],
                "albums": list,
                "lifeSpan" : entry.get("lifeSpan"),
                "deezerFans": artist_deezerFans,
                "members" : list_members
                }
                print(data)
                names_genres.append(data)
        time.sleep(1)
        print("pause")
        number += 200
        number_str = str(number)



    # Enregistrer les données dans un fichier JSON (écrasée ou crée)
    file_path = "data/artist_all.json"
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(names_genres, json_file, ensure_ascii=False, indent=4)

    return names_genres


def fetch_details():
    with open('data/artist_all.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    genres = ["Blues", "Country", "Electronic", "Folk", "Hip Hop", "Jazz"]

    for genre in genres:
        nbr_groupes = 0
        nbr_solos = 0
        nbr_actif = 0

        for item in data:
            if genre in item.get("genres", []):
                if item["type"] == "Group":
                    nbr_groupes += 1
                elif item["type"] == "Person":
                    nbr_solos += 1
                elif item["type"] is None:
                    if item["nombre_members"] > 1:
                        nbr_groupes += 1
                    else:
                        nbr_solos += 1

                if not item["lifeSpan"]["ended"]:
                    nbr_actif += 1

            genre_info = {
            "nombre_groupes": nbr_groupes,
            "nombre_solos": nbr_solos,
            "nombre_actifs": nbr_actif
            }

        print(f"nombre groupe pour le genre {genre} : {nbr_groupes}")
        print(f"nombre solo pour le genre {genre} : {nbr_solos}")
        print(f"nombre actifs pour le genre {genre} : {nbr_actif}")

        with open(f"data/details/{genre}.json", 'w') as genre_file:  # Utilisez 'w' pour écraser le fichier
            json.dump(genre_info, genre_file, indent=4)















