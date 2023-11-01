from flask import Flask, request, jsonify
import functions
from functions import FilterType

app = Flask(__name__, instance_relative_config=True)




@app.route('/api/filter_artists', methods=['GET'])
def api_filter_artists():
    genre = request.args.get('genre')
    subgenre = request.args.get('subgenre')
    filter_type = request.args.get('filter_type', FilterType.NONE)
    filter_value = request.args.get('filter_value')
    limit = request.args.get('limit')

    artists = functions.filter_artists(genre, subgenre, filter_type, filter_value, limit)

    return jsonify(artists)


if __name__ == '__main__':
    app.run()
