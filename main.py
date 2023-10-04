import functions
url = "https://wasabi.i3s.unice.fr"

def main():


    # Paramètres de la requête
    params = {    }

    # Appel de la fonction pour récupérer les données de l'API
    popularity_data = functions.fetch_genre_popularity(url)

    genre_data = functions.fetch_genre_song(url)

    if popularity_data:
        # Utilisez les données récupérées comme bon vous semble
        print(popularity_data)

    if genre_data :

        print(genre_data)


if __name__ == "__main__":
    main()