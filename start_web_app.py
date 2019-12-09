from flask import Flask
from flask import request
from flask import jsonify
import graph as g
import helper as hl
from pprint import pprint

graph = g.Graph(hl.Helper().load_structure('data.json'))
app = Flask(__name__)

@app.route('/')
def index():
    return ok('Welcome to wiki-scrappy Web API!')

@app.errorhandler(400)
def not_found(error=None):
    message = {
        'status': 400,
        'message': 'Bad Request: ' + request.url
    }
    response = jsonify(message)
    response.status_code = 400
    return response

def ok(data):
    response = jsonify(data)
    response.status_code = 200
    return response

def created(data):
    response = jsonify(data)
    response.status_code = 201
    return response

@app.route('/actors', methods=['GET'])
def actor_attr():
    try:
        if(request.args.get('name', None) != None):
            name = str(request.args.get('name', None)).lower()
            return ok(graph.filter_actors('name', name))
        if(request.args.get('age', None) != None):
            age = str(request.args.get('age', None))
            return ok(graph.filter_actors('age', age))
        if(request.args.get('grossing', None) != None):
            grossing = str(request.args.get('grossing', None))
            return ok(graph.filter_actors('grossing', grossing))
        if(request.args.get('movies', None) != None):
            movies = request.args.get('movies', None)
            movies = str(movies).split(',')
            return ok(graph.filter_actors('movies', movies))
        return 'done'
    except:
        return not_found()

@app.route('/movies', methods=['GET'])
def movie_attr():
    try:
        if(request.args.get('name', None) != None):
            name = str(request.args.get('name', None)).lower()
            return ok(graph.filter_movies('name', name))
        if(request.args.get('release_date', None) != None):
            release_date = str(request.args.get('release_date', None))
            return ok(graph.filter_movies('release_date', release_date))
        if(request.args.get('grossing', None) != None):
            grossing = str(request.args.get('grossing', None))
            return ok(graph.filter_movies('grossing', grossing))
        if(request.args.get('actors', None) != None):
            actors = request.args.get('actors', None)
            actors = str(actors).split(',')
            return ok(graph.filter_movies('actors', actors))
        return 'done'
    except:
        return not_found()

@app.route('/actors/<actor_name>', methods=['GET'])
def actor(actor_name):
    actor_name = str(actor_name).lower()
    result = graph.get_actor_object(actor_name)
    if result != -1:    
        return ok(result)
    else:
        return not_found()

@app.route('/movies/<movie_name>', methods=['GET'])
def movie(movie_name):
    movie_name = str(movie_name).lower()
    result = graph.get_movie_object(movie_name)
    if result != -1:    
        return ok(result)
    else:
        return not_found()

@app.route('/actors/<actor_name>', methods=['PUT'])
def actor_put(actor_name):
    actor_name = str(actor_name).lower()
    actor_name = actor_name.replace('_', ' ')
    if not request.json:
        return not_found()
    if not 'age' in request.json:
        return not_found()
    try:
        age = str(request.json['age'])
        graph.get_graph()[actor_name][0] = (age,)
        return ok(graph.get_actor_object(actor_name))
    except:
        return not_found()
    
@app.route('/movies/<movie_name>', methods=['PUT'])
def movie_put(movie_name):
    movie_name = str(movie_name).lower()
    movie_name = movie_name.replace('_', ' ')
    if not request.json:
        return not_found()
    if not 'release_date' in request.json and not 'grossing' in request.json:
        return not_found()
    try:
        if 'release_date' in request.json:
            release_date = str(request.json['release_date'])
            (oldrelease_date, grossing) = graph.get_graph()[movie_name][0]
            graph.get_graph()[movie_name][0] = (release_date, grossing)
            return ok(graph.get_movie_object(movie_name))
        else:
            grossing = str(request.json['grossing'])
            (release_date, oldgrossing) = graph.get_graph()[movie_name][0]
            graph.get_graph()[movie_name][0] = (release_date, grossing)
            return ok(graph.get_movie_object(movie_name))
    except:
        return not_found()
    
@app.route('/actors', methods=['POST'])
def actor_post():
    if not request.json:
        return not_found()
    if not 'name' in request.json:
        return not_found()
    try:
        actor_name = str(request.json['name']).lower()
        graph.get_graph()[actor_name] = [('0',)]
        return created(graph.get_actor_object(actor_name))
    except:
        return not_found()
    
@app.route('/movies', methods=['POST'])
def movie_post():
    if not request.json:
        return not_found()
    if not 'name' in request.json:
        return not_found()
    try:
        movie_name = str(request.json['name']).lower()
        graph.get_graph()[movie_name] = [('2017-10-16', '0')]
        return created(graph.get_movie_object(movie_name))
    except:
        return not_found()
    
@app.route('/actors/<actor_name>', methods=['DELETE'])
def actor_delete(actor_name):
    actor_name = str(actor_name).lower()
    actor_name = actor_name.replace('_', ' ')
    if graph.get_graph().has_key(actor_name):
        graph.get_graph().pop(actor_name, None)
        return ok(graph.get_actor_object(actor_name))
    else:
        return not_found()
    
@app.route('/movies/<movie_name>', methods=['DELETE'])
def movie_delete(movie_name):
    movie_name = str(movie_name).lower()
    movie_name = movie_name.replace('_', ' ')
    if graph.get_graph().has_key(movie_name):
        graph.get_graph().pop(movie_name, None)
        return ok(graph.get_movie_object(movie_name))
    else:
        return not_found()

if __name__ == '__main__':
    app.run(debug=True)