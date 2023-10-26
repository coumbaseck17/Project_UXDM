
import functions
url = "https://wasabi.i3s.unice.fr"

#enums pas encore utilisé
from enum import Enum

class Genre(Enum):
    ROCK = "Rock"
    POP = "Pop"
    FOLK = "Folk"
    HIP_HOP = "Hip Hop"
    ELECTRONIC = "Electronic"
    BLUES = "Blues"
    RNB = "R&B"
    JAZZ = "Jazz"
    COUNTRY = "Country"

class Subgenre(Enum):
    # Rock
    ALL = "all"
    ROCK = "Rock"
    ALTERNATIVE_ROCK = "Alternative Rock"
    INDIE_ROCK = "Indie Rock"
    HEAVY_METAL = "Heavy Metal"
    HARD_ROCK = "Hard Rock"
    PUNK_ROCK = "Punk Rock"
    PROGRESSIVE_ROCK = "Progressive Rock"
    FOLK_ROCK = "Folk Rock"
    ROCK_N_ROLL = "Rock 'N' Roll"
    CLASSIC_ROCK = "Classic Rock"
    HARD_METAL = "Heavy Metal"

    # Pop
    POP = "Pop"
    SINGER_SONGWRITER = "Singer-Songwriter"
    POP_ROCK = "Pop Rock"
    INDIE_POP = "Indie Pop"
    DANCE_POP = "Dance-Pop"
    ELECTROPOP = "Electropop"

    # Folk
    FOLK = "Folk"
    CONTEMPORARY_FOLK = "Contemporary Folk"
    INDIE_FOLK = "Indie Folk"
    PROGRESSIVE_FOLK = "Progressive Folk"
    PSYCH_FOLK = "Psych Folk"

    # Hip Hop
    HIP_HOP = "Hip Hop"

    # Electronic
    ELECTRONIC = "Electronic"
    HOUSE = "House"
    TECHNO = "Techno"

    # Blues
    BLUES = "Blues"
    BLUES_ROCK = "Blues Rock"

    # R&B
    SOUL = "Soul"
    RNB = "R&B"
    FUNK = "Funk"

    # Jazz
    SWING = "Swing"
    JAZZ = "Jazz"

    # Country
    COUNTRY = "Country"
    COUNTRY_ROCK = "Country Rock"
    COUNTRY_POP = "Country Pop"

class FilterType(Enum):
    NONE = "NONE"
    TYPE = "TYPE"
    GENDER = "GENDER"

class FilterValue(Enum):
    TYPE_GROUP = "Group"
    TYPE_PERSON = "Person"
    GENDER_FEMALE = "Female"
    GENDER_MALE = "Male"

def main():


    """Appel de la fonction pour récupérer les données de l'API"""
    #popularity_data = functions.fetch_genre_popularity(url)

    # artist_data = functions.fetch_artists_all(url)
    #
    # if artist_data:
    #
    #     print(artist_data)

    # functions.fetch_artists_by_genre()

    #functions.fetch_info_artist(url)
    #functions.fetch_genre_details_ALL()
    #functions.fetch_details_others()
    #functions.fetch_artists_genre()
    #functions.fetch_genre_details_ALL()

    #functions.create_genre_all_files()




    artists=functions.filter_artists("Rock","all","GENDER","Female",1)
    print(artists)



if __name__ == "__main__":
    main()
