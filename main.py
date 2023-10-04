import time

import functions
url = "https://wasabi.i3s.unice.fr"
import json

def main():


    # Paramètres de la requête
    params = {
        "limit": "10"
    }

    # Appel de la fonction pour récupérer les données de l'API
    popularity_data = functions.fetch_genre_popularity(url)

    if popularity_data:
        # Utilisez les données récupérées comme bon vous semble
        print(popularity_data)



    min_artists_per_genre = 10

    # Charger le document JSON de popularité des genres
    with open("data/popularity.json", "r", encoding="utf-8") as json_file:
        popularity_data = json.load(json_file)

    # Liste pour stocker les artistes
    all_artists = []

    # Boucler à travers les genres et récupérer les artistes
    for genre_info in popularity_data:
        genre_name = genre_info["_id"]
        while len(all_artists) < min_artists_per_genre:
            artists = functions.fetch_artists_by_genre( genre_name)
            if artists:
                all_artists.extend(artists)
    # Vous avez maintenant au moins 100 artistes par genre dans la liste all_artists.
    # Vous pouvez faire d'autres traitements ou afficher les résultats ici.


if __name__ == "__main__":
    main()
