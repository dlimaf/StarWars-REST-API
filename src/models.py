from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250),unique=True,nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "email": self.email,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String, nullable=True)
    eye_color = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "eye_color" : self.eye_color
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=True)
    population = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate":self.climate,
            "population" : self.population
        }

class Starships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=True)
    starship_class = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Starships %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model":self.model,
            "starship_class" : self.starship_class
        }

class FavoritesCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user = db.relationship("User")
    characters = db.relationship("Characters")

    def __repr__(self):
        return '<FavoritesCharacters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id":self.characters_id
        }

class FavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.relationship("User")
    planets = db.relationship("Planets")

    
    def __repr__(self):
        return '<FavoritesPlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id":self.planets_id
        }

class FavoritesStarships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    starships_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
    user = db.relationship("User")
    starships = db.relationship("Starships")

        
    def __repr__(self):
        return '<FavoritesStarships %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starships_id":self.starships_id
        }