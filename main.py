import time

import functions
url = "https://wasabi.i3s.unice.fr"
import json

def main():


    """Appel de la fonction pour récupérer les données de l'API"""
    popularity_data = functions.fetch_genre_popularity(url)

    if popularity_data:

        print(popularity_data)

    # functions.fetch_artists_by_genre()

    functions.fetch_info_artist(url)



if __name__ == "__main__":
    main()
