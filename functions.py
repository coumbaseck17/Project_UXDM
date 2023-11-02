import os
import urllib
import time
from enum import Enum
import requests
import json

class FilterType(Enum):
    NONE = "NONE"
    TYPE = "TYPE"
    GENDER = "GENDER"

url = "https://wasabi.i3s.unice.fr"
params = {}


"""
    Cette fonction permet d'effectuer une requête GET à l'API avec les paramètres spécifiés.
"""

def api_request(url, endpoint, params):
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


"""
    Cette fonction permet de récupérer la liste des GENRES les plus populaires.
"""

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


"""
    Cette fonction permet de récupérer les noms des artistes en fonction d'un genre depuis l'API Wasabi.
"""


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



"""
    Cette fonction permet de récupérer la liste de tous les artistes existants de WASABI.
"""
def fetch_artists_all(url):
    number = 1
    names_genres = []
    number_str = str(number)
    while (number < 77492):
        endpoint = "/api/v1/artist_all/" + number_str
        request = api_request(url, endpoint, {})
        print(endpoint)
        for entry in request:
            artist_deezerFans = entry.get("deezerFans")
            if (artist_deezerFans is not None and artist_deezerFans != 0):

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
                    "nombre_members": nombre_members,
                    "recordLabel": entry.get("recordLabel"),
                    "urlDeezer": entry.get("urlDeezer"),
                    "gender": entry.get("gender"),
                    "picture": entry["picture"]["standard"],
                    "albums": list,
                    "lifeSpan": entry.get("lifeSpan"),
                    "deezerFans": artist_deezerFans,
                    "members": list_members
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


"""
    Cette fonction permet de stocker dans un fichier les statistiques de chaque genre et sous-genre.
"""
def fetch_details():
    with open('data/artist_all.json', 'r', encoding='utf-8') as json_file:
        dataArtist = json.load(json_file)

    with open('data/genre_subgenre.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for genre, subgenres in data.items():
        # créer un répertoire pour le genre
        genre_dir = os.path.join('data/details', genre)
        os.makedirs(genre_dir, exist_ok=True)

        for subgenre in subgenres:
            nbr_groupes = 0
            nbr_solos = 0
            nbr_actif = 0

            for item in dataArtist:
                if subgenre in item.get("genres", []):
                    if item["type"] == "Group":
                        nbr_groupes += 1
                    elif item["type"] == "Person":
                        nbr_solos += 1

                    if not item["lifeSpan"]["ended"]:
                        nbr_actif += 1

            total_artists = nbr_groupes + nbr_solos
            if total_artists > 0:
                pourcentage_actif = int((nbr_actif / total_artists) * 100)
            else:
                pourcentage_actif = 0

            subgenre_info = {
                "nombre_groupes": nbr_groupes,
                "nombre_solos": nbr_solos,
                "nombre_actif": nbr_actif,
                "pourcentage_actifs": pourcentage_actif
            }

            subgenre_file = os.path.join(genre_dir, f'{subgenre}.json')
            with open(subgenre_file, 'w', encoding="utf-8") as output_file:
                json.dump(subgenre_info, output_file, indent=4)



"""
    Cette fonction permet de stocker dans un fichier les statistiques sur les artistes de tous les genres confondus.
"""
def fetch_details_others():
    with open('data/artist_all.json', 'r', encoding='utf-8') as json_file:
        dataArtist = json.load(json_file)

    nbr_groupes = 0
    nbr_solos = 0
    nbr_actif = 0

    for item in dataArtist:
        genres = item.get("genres")
        if not genres:
            print(f"Artist: {item['name']}, Genres: {genres}")
            if item["type"] == "Group":
                nbr_groupes += 1
            elif item["type"] == "Person":
                nbr_solos += 1
            if not item["lifeSpan"]["ended"]:
                nbr_actif += 1

    total_artists = nbr_groupes + nbr_solos
    if total_artists > 0:
        pourcentage_actif = int((nbr_actif / total_artists) * 100)
    else:
        pourcentage_actif = 0

    others_info = {
        "nombre_groupes": nbr_groupes,
        "nombre_solos": nbr_solos,
        "nombre_actif": nbr_actif,
        "pourcentage_actifs": pourcentage_actif
    }

    genre_dir = 'data/details'
    others_file = os.path.join(genre_dir, 'Others.json')
    with open(others_file, 'w', encoding="utf-8") as output_file:
        json.dump(others_info, output_file, indent=4)



"""
    Cette fonction permet de stocker dans un dossier des fichiers pour chaque genre et sous-genre 
    une liste d'artistes ordonnée selon l'attribut deezerFans.
"""
# récupérer les artistes par genre & sous-genre et les trier par popularité
def organize_and_sort_artists():
    with open('data/genre_subgenre.json', 'r', encoding='utf-8') as json_file:
        genre_data = json.load(json_file)

    with open('data/artist_all.json', 'r', encoding='utf-8') as json_file:
        artist_data = json.load(json_file)

    artists_by_genre = {genre: {subgenre: [] for subgenre in subgenres} for genre, subgenres in genre_data.items()}

    for artist in artist_data:
        artist_genres = artist.get("genres", [])
        artist_type = artist.get("type", "Unknown")  # Si le type est manquant, utilisez "Unknown"

        for genre, subgenres in genre_data.items():
            for subgenre in subgenres:
                if subgenre in artist_genres:
                    artists_by_genre[genre][subgenre].append(artist)

    def classify_artists_by_deezer_fans(artists_by_genre):
        sorted_artists = {}

        for genre, subgenres_data in artists_by_genre.items():
            sorted_artists[genre] = {}
            for subgenre, artists in subgenres_data.items():
                sorted_artists[genre][subgenre] = sorted(artists, key=lambda x: x.get("deezerFans", 0), reverse=True)

        return sorted_artists

    sorted_artists_by_deezer_fans = classify_artists_by_deezer_fans(artists_by_genre)

    output_dir = 'data/artists_by_genre_sorted_v1'
    os.makedirs(output_dir, exist_ok=True)

    for genre, subgenres_data in sorted_artists_by_deezer_fans.items():
        genre_dir = os.path.join(output_dir, genre)
        os.makedirs(genre_dir, exist_ok=True)

        for subgenre, artists in subgenres_data.items():
            filename = os.path.join(genre_dir, f'{subgenre}.json')
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(artists, json_file, ensure_ascii=False, indent=4)
    # Enregistrez tous les artistes du genre triés par nombre de deezerFans
    # Enregistrez tous les artistes du genre triés par nombre de deezerFans
    for genre, subgenres_data in sorted_artists_by_deezer_fans.items():
        genre_artists = []  # Utilisez une liste pour stocker les artistes
        artist_ids = set()  # Utilisez un ensemble pour éviter les doublons

        for subgenre, artists in subgenres_data.items():
            for artist in artists:
                if artist["id"] not in artist_ids:
                    artist_ids.add(artist["id"])
                    genre_artists.append(artist)

        genre_dir = os.path.join(output_dir, genre)
        filename = os.path.join(genre_dir, f'{genre}_all_artists_sorted.json')

        # Triez la liste par nombre de deezerFans
        genre_artists_sorted = sorted(genre_artists, key=lambda x: x.get("deezerFans", 0), reverse=True)

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(genre_artists_sorted, json_file, ensure_ascii=False, indent=4)


"""
    Cette fonction est une version ameliorée de la méthode précédente fetch_details : 
        - on ne s'appuie plus sur le fichier artiste_all mais sur les fichiers JSON stockées dans le dossier
        "data/artists_by_genre_sorted".
        -on stockes plus de statistiques. 
"""
def fetch_details_artists_sorted():
    with open('data/genre_subgenre.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for genre, subgenres in data.items():
        for subgenre in subgenres:
            genre_dir = os.path.join('data/artists_by_genre_sorted_v1', genre)
            subgenre_file = os.path.join(genre_dir, f'{subgenre}.json')

            with open(subgenre_file, 'r', encoding='utf-8') as json_file:
                artists = json.load(json_file)

            unique_artists = {}

            for artist in artists:
                artist_id = artist["id"]
                if artist_id not in unique_artists:
                    unique_artists[artist_id] = artist

            nbr_groupes = 0
            nbr_solos = 0
            nbr_actif = 0
            nbr_autres= 0
            nbr_actif_group = 0
            nbr_actif_autres = 0
            nbr_actif_solos = 0

            for item in unique_artists.values():
                if item["type"] == "Group":
                    nbr_groupes += 1
                    if not item["lifeSpan"]["ended"]:
                        nbr_actif_group += 1
                        nbr_actif += 1
                elif item["type"] == "Person":
                    nbr_solos += 1
                    if not item["lifeSpan"]["ended"]:
                        nbr_actif_solos += 1
                        nbr_actif += 1
                else:
                    nbr_autres += 1
                    if not artist["lifeSpan"]["ended"]:
                        nbr_actif_autres += 1
                        nbr_actif += 1

            total_artists = nbr_groupes + nbr_solos + nbr_autres
            if total_artists > 0:
                pourcentage_actif = int((nbr_actif / total_artists) * 100)
            else:
                pourcentage_actif = 0

            subgenre_info = {
                "nombre_artists_total": total_artists,
                "nombre_groupes": nbr_groupes,
                "nombre_solos": nbr_solos,
                "nombre_autres": nbr_autres,
                "nombre_actif_groupes": nbr_actif_group,
                "nombre_actif_solos": nbr_actif_solos,
                "nombre_actif_total": nbr_actif,
                "nombre_actif_autres": nbr_actif_autres,
                "pourcentage_actifs": pourcentage_actif
            }

            subgenre_dir = os.path.join('data/details_v1', genre)
            os.makedirs(subgenre_dir, exist_ok=True)

            subgenre_file = os.path.join(subgenre_dir, f'{subgenre}.json')
            with open(subgenre_file, 'w', encoding="utf-8") as output_file:
                json.dump(subgenre_info, output_file, indent=4)

"""
    Cette fonction permet de stocker dans un fichier les statistiques d'un $GENRE
    (on rassemble tous les statistiques des sous-genre du $GENRE mais on compte pas les artistes plusieurs fois dans le 
    cas ou ils possèdent plusieurs sous-genre dans le $GENRE.
"""

def fetch_genre_details_ALL():
    with open('data/genre_subgenre.json', 'r', encoding='utf-8') as json_file:
        genre_data = json.load(json_file)

    for genre, subgenres in genre_data.items():
        genre_dir = os.path.join('data/artists_by_genre_sorted_v1', genre)
        genre_all_file = os.path.join(genre_dir, f'{genre}_all_artists_sorted.json')

        with open(genre_all_file, 'r', encoding='utf-8') as json_file:
            artists = json.load(json_file)

        unique_artists = {}

        for artist in artists:
            artist_id = artist["id"]
            if artist_id not in unique_artists:
                unique_artists[artist_id] = artist

        nbr_groupes = 0
        nbr_solos = 0
        nbr_actif = 0
        nbr_actif_group = 0
        nbr_actif_solos = 0
        nbr_actif_autres =0
        nbr_autres =0

        for artist in unique_artists.values():

            if artist["type"] == "Group":
                nbr_groupes += 1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_group += 1
                    nbr_actif += 1
            elif artist["type"] == "Person":
                nbr_solos += 1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_solos += 1
                    nbr_actif += 1
            else:
                nbr_autres +=1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_autres +=1
                    nbr_actif += 1



        total_artists = len(unique_artists)
        if total_artists > 0:
            pourcentage_actif = int((nbr_actif / total_artists) * 100)
        else:
            pourcentage_actif = 0


        total_artists = len(unique_artists)
        print(f"Genre: {genre}")
        print(f"Nombre total d'artistes : {total_artists}")

        genre_info = {
            "nombre_artists_total": total_artists,
            "nombre_groupes": nbr_groupes,
            "nombre_solos": nbr_solos,
            "nombre_autres": nbr_autres,
            "nombre_actif_groupes": nbr_actif_group,
            "nombre_actif_solos": nbr_actif_solos,
            "nombre_actif_total": nbr_actif,
            "nombre_actif_autres": nbr_actif_autres,
            "pourcentage_actifs": pourcentage_actif
        }

        total_artists = len(unique_artists)

        print(f"Genre: {genre}")
        print(f"Nombre total d'artistes : {total_artists}")

        details_dir = os.path.join('data/details_v1', genre)
        os.makedirs(details_dir, exist_ok=True)
        genre_info_file = os.path.join(details_dir, f'{genre}_details.json')
        with open(genre_info_file, 'w', encoding='utf-8') as json_file:
            json.dump(genre_info, json_file, ensure_ascii=False, indent=4)



"""
    Cette fonction est une fonction utilisé par la méthode consolidate_genre_details pour récupérer les détails 
    d'un GENRE (et non pas d'un sous-genre)
"""
def fetch_genre_details_ALL_folder(genreFolder):
    with open('data/genre_subgenre.json', 'r', encoding='utf-8') as json_file:
        genre_data = json.load(json_file)

    for genre, subgenres in genre_data.items():
        genre_dir = os.path.join('data/artists_by_genre_sorted_v1', genreFolder)
        genre_all_file = os.path.join(genre_dir, f'{genreFolder}_all_artists_sorted.json')

        with open(genre_all_file, 'r', encoding='utf-8') as json_file:
            artists = json.load(json_file)

        unique_artists = {}

        for artist in artists:
            artist_id = artist["id"]
            if artist_id not in unique_artists:
                unique_artists[artist_id] = artist

        nbr_groupes = 0
        nbr_solos = 0
        nbr_actif = 0
        nbr_actif_group = 0
        nbr_actif_solos = 0
        nbr_actif_autres = 0
        nbr_autres = 0

        for artist in unique_artists.values():

            if artist["type"] == "Group":
                nbr_groupes += 1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_group += 1
                    nbr_actif += 1
            elif artist["type"] == "Person":
                nbr_solos += 1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_solos += 1
                    nbr_actif += 1
            else:
                nbr_autres += 1
                if not artist["lifeSpan"]["ended"]:
                    nbr_actif_autres += 1
                    nbr_actif += 1

        total_artists = len(unique_artists)
        if total_artists > 0:
            pourcentage_actif = int((nbr_actif / total_artists) * 100)
        else:
            pourcentage_actif = 0

        total_artists = len(unique_artists)
        print(f"Genre: {genre}")
        print(f"Nombre total d'artistes : {total_artists}")

        genre_info = {
            "nombre_artists_total": total_artists,
            "nombre_groupes": nbr_groupes,
            "nombre_solos": nbr_solos,
            "nombre_autres": nbr_autres,
            "nombre_actif_groupes": nbr_actif_group,
            "nombre_actif_solos": nbr_actif_solos,
            "nombre_actif_total": nbr_actif,
            "nombre_actif_autres": nbr_actif_autres,
            "pourcentage_actifs": pourcentage_actif
        }

        total_artists = len(unique_artists)

        print(f"Genre: {genre}")
        print(f"Nombre total d'artistes : {total_artists}")


    return genre_info



"""
    Cette fonction permet de récupérer les artistes selon 
    -genre : le GENRE, exemple => "Rock"
    -subgenre_or_all : le subgenre, exemple => "Pop Rock" mais aussi peut être égal à "all" si on veut récupérer
     les artistes de tous les sous-genres confondus du GENRE spécifié dans le premier paramètre 
    -filter_type : le type de Filtre : "type" ou "gender"
    -filter_value :la valeur du Filtre : "person" ou "group" ou "" si filter_type= "type" , 
    "female" ou "male" si filter_type="gender" 
"""


def filter_artists(genre, subgenre_or_all, filter_type=None, filter_value=None, limit=None):
    if subgenre_or_all == "all" or subgenre_or_all is None:
        file_path = f"data/artists_by_genre_sorted_v1/{genre}/{genre}_all_artists_sorted.json"
    else:
        file_path = f"data/artists_by_genre_sorted_v1/{genre}/{subgenre_or_all}.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            artists = json.load(json_file)

        if filter_type is not None and filter_value is not None:
            filtered_artists = []
            for artist in artists:
                if filter_type == "TYPE":
                    if artist.get("type") == filter_value:
                        filtered_artists.append(artist)
                elif filter_type == "GENDER":
                    if artist.get("gender") == filter_value:
                        filtered_artists.append(artist)
            return filtered_artists
        else:
            return artists
    except FileNotFoundError:
        return []


"""
    Cette fonction permet de regrouper toutes les statistiques des GENRES et SOUS-GENRES dans un seul fichier
    -en se basant sur les fichiers (contenant les statistiques) d'un dossier données en entrée : data_directory
    -et stocke les données dans le fichier dont le chemin est donné en paramètre : output_file
"""

def consolidate_genre_details(data_directory, output_file):
    consolidated_data = {"genres": {}}

    for genre_folder in os.listdir(data_directory):
        genre_path = os.path.join(data_directory, genre_folder)

        if os.path.isdir(genre_path):
            genre_details = fetch_genre_details_ALL_folder(genre_folder)

            subgenre_data = {}

            for subgenre_file in os.listdir(genre_path):
                if subgenre_file.endswith(".json") and not subgenre_file.endswith("details.json") and subgenre_file != f"{genre_folder}_all.json":
                    subgenre_name = os.path.splitext(subgenre_file)[0]
                    subgenre_file_path = os.path.join(genre_path, subgenre_file)

                    with open(subgenre_file_path, "r", encoding="utf-8") as json_file:
                        subgenre_details = json.load(json_file)

                    subgenre_data[subgenre_name] = {"details": subgenre_details}

            consolidated_data["genres"][genre_folder] = {
                "details": genre_details,
                "subgenres": subgenre_data
            }

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(consolidated_data, json_file, ensure_ascii=False, indent=4)

    print(f"Fichier JSON consolidé créé avec succès dans {output_file}")


