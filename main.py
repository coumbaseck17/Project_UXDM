
import functions
url = "https://wasabi.i3s.unice.fr"

def main():


    """Appel de la fonction pour récupérer les données de l'API"""

""""" Appel fonctions déjà appelées
    functions.fetch_details_artists_sorted()
    functions.fetch_genre_details_ALL()
    data_directory = "data/details_v1"
    output_file = "data/details_v1/all_data_details.json"
    functions.consolidate_genre_details(data_directory, output_file)
    functions.fetch_details_artists_sorted()
"""
artists =functions.filter_artists("Rock","Punk Rock","TYPE","")
print(artists)
functions.fetch_details_others()
if __name__ == "__main__":
    main()
