import json

from flask import Flask, request, jsonify
import functions

app = Flask(__name__, instance_relative_config=True)

"""
  Pour tester les routes : 
    1) Taper la commande python ./app.py sur le terminal
    2) Aller su postaman ou directement sur le navigateur (si postaman aller APPLICATION POSTMAN et non pas 
    sur postman navigateur)
    3) Requête GET artistes :
    localhost:5000/api/filter_artists?genre=Rock&subgenre=all" 
    localhost:5000/api/filter_artists?genre=Rock&subgenre=Punk Rock&filter_type=TYPE&filter_value= 
    #affiche artistes qui ne sont ni group ni person dans Punk Rock
    localhost:5000/api/filter_artists?genre=Rock&subgenre=Punk Rock&filter_type=TYPE&filter_value=Group
    localhost:5000/api/filter_artists?genre=Rock&subgenre=Punk Rock&filter_type=GENDER&filter_value=Female
    Requête GET statistiques:
    localhost:5000/api/statistiques
    
"""


@app.route('/api/filter_artists', methods=['GET'])
def api_filter_artists():
    genre = request.args.get('genre')
    subgenre = request.args.get('subgenre')
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')
    limit = request.args.get('limit')

    artists = functions.filter_artists(genre, subgenre, filter_type, filter_value, limit)

    return jsonify(artists)


@app.route('/api/statistiques', methods=['GET'])
def get_data():
    with open('data/details_v1/all_data_details.json', 'r') as json_file:
        data = json.load(json_file)
    print(data)
    return jsonify(data)

@app.route('/api/statistiques/others', methods=['GET'])
def get_data_others():
    with open('data/details_v1/Others.json', 'r') as json_file:
        data = json.load(json_file)
    print(data)
    return jsonify(data)



if __name__ == '__main__':
    app.run()
