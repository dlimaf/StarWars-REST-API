"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, FavoritesCharacters, FavoritesPlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def getUsers():
    all_users = User.query.all()
    result = list(map(lambda users: users.serialize(),all_users))
    return jsonify(result)

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def getUsersFavorites(user_id):
    fav_characters = FavoritesCharacters.query.filter_by(user_id=user_id)
    fav_planets = FavoritesPlanets.query.filter_by(user_id=user_id)
    print(fav_characters)
    result1 = list(map(lambda userfavoritescharacters: userfavoritescharacters.serialize(), fav_characters))
    result2 = list(map(lambda userfavoritesplanets: userfavoritesplanets.serialize(), fav_planets))
    return jsonify(result1,result2)

@app.route('/characters', methods=['GET'])
def getCharacters():
    all_characters = Characters.query.all()
    print(all_characters)
    result = list(map(lambda characters: characters.serialize(),all_characters))

    return jsonify(result)

@app.route('/characters/<int:characters_id>', methods=['GET'])
def getCharactersId(characters_id):
    one_character = Characters.query.get(characters_id)
    print(one_character)
    if one_character is None:
        return jsonify({"mensaje":"no existe"}), 404
    else: 
        return jsonify(one_character.serialize())

@app.route('/characters', methods=['POST'])
def add_character():
    body= request.get_json()
    new_character = Characters(name=body['name'], gender=body['gender'], eye_color=body['eye_color'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"mensaje":"personaje agregado"}),201

@app.route('/favorite/character/<int:characters_id>', methods=['POST'])   
def add_favorite_character(characters_id):
    body = request.get_json()
    character = Characters.query.get(characters_id)
    user = User.query.get(body['user_id'])
    new_favorite_character = FavoritesCharacters(user_id=body['user_id'],characters_id=characters_id)
    if not character or not user:
        return jsonify({"msg":"character or user does not exist"})
    if FavoritesCharacters.query.filter_by(user_id=body['user_id'],characters_id=characters_id).first():
        return jsonify({"msg":"the character is already added to your favorites"})
    else:
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify(new_favorite_character.serialize())
    
@app.route('/favorite/character/<int:characters_id>', methods=['DELETE'])   
def delete_favorite_character(characters_id):
    body = request.get_json()
    favorite_character = FavoritesCharacters.query.filter_by(user_id=body['user_id'],characters_id=characters_id).first()
    if favorite_character is None:
        return jsonify({"msg":"this character is not among your favorites"})
    else:
        db.session.delete(favorite_character)
        db.session.commit()
        return jsonify({"msg":"favorite removed"})


@app.route('/planets', methods=['GET'])
def getPlanets():
    all_planets = Planets.query.all()
    result = list(map(lambda planets: planets.serialize(),all_planets))

    return jsonify(result)

@app.route('/planets/<int:planets_id>', methods=['GET'])
def getPlanetsId(planets_id):
    one_planet = Planets.query.get(planets_id)
    if one_planet is None:
        return jsonify({"mensaje":"no existe"}), 404
    else: 
        return jsonify(one_planet.serialize())
    
@app.route('/planets', methods=['POST'])
def add_planet():
    body= request.get_json()
    new_planet = Planets(name=body['name'], climate=body['climate'], population=body['population'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"mensaje":"personaje agregado"}),201

@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])   
def add_favorite_planet(planets_id):
    body = request.get_json()
    planet = Planets.query.get(planets_id)
    user = User.query.get(body['user_id'])
    new_favorite_planet = FavoritesPlanets(user_id=body['user_id'],planets_id=planets_id)
    if not planet or not user:
        return jsonify({"msg":"planet or user does not exist"})
    if FavoritesPlanets.query.filter_by(user_id=body['user_id'],planets_id=planets_id).first():
        return jsonify({"msg":"the planet is already added to your favorites"})
    else:
        db.session.add(new_favorite_planet)
        db.session.commit()
        return jsonify(new_favorite_planet.serialize())

@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])   
def delete_favorite_planet(planets_id):
    body = request.get_json()
    favorite_planet = FavoritesPlanets.query.filter_by(user_id=body['user_id'],planets_id=planets_id).first()
    if favorite_planet is None:
        return jsonify({"msg":"this planet is not among your favorites"})
    else:
        db.session.delete(favorite_planet)
        db.session.commit()
        return jsonify({"msg":"favorite removed"})

"""
@app.route('/favorites/<id>', methods=['DELETE'])
def delete_favorite(id):
    favorite1 = FavoritesPlanets.query.get(id)
    favorite2 = FavoritesCharacters.query.get(id)
    if favorite1:
        favorite = favorite1
        db.session.delete(favorite)
        db.session.commit()
        return jsonify(favorite.serialize())
    if favorite2:
        favorite = favorite2
        db.session.delete(favorite)
        db.session.commit()
        return jsonify(favorite.serialize())
        
    return jsonify({"mensaje":"personaje eliminado"})

"""
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
