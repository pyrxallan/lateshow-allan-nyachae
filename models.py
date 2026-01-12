from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()



class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    def to_dict(self, fields=None, include_appearances=False):
        base = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        if fields:
            return {k: base[k] for k in fields}
        if include_appearances:
            base['appearances'] = [a.to_dict(include_guest=True, include_episode=False) for a in self.appearances]
        return base


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=True)

    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    def to_dict(self, fields=None):
        base = {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }
        if fields:
            return {k: base[k] for k in fields}
        return base


class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    @validates('rating')
    def validate_rating(self, key, value):
        if value is None:
            raise ValueError('rating must be present')
        try:
            v = int(value)
        except Exception:
            raise ValueError('rating must be an integer')
        if v < 1 or v > 5:
            raise ValueError('rating must be between 1 and 5')
        return v

    def to_dict(self, include_guest=False, include_episode=False):
        base = {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id
        }
        if include_guest:
            base['guest'] = self.guest.to_dict()
        if include_episode:
            base['episode'] = self.episode.to_dict(fields=('id','date','number'))
        return base


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('name must be present')
        if len(value) < 1 or len(value) > 100:
            raise ValueError('name must be between 1 and 100 characters')
        return value

    @validates('address')
    def validate_address(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('address must be present')
        return value

    def to_dict(self, include_pizzas=False):
        base = {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
        if include_pizzas:
            base['restaurant_pizzas'] = [rp.to_dict(include_restaurant=False) for rp in self.restaurant_pizzas]
        return base


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('name must be present')
        if len(value) < 1 or len(value) > 100:
            raise ValueError('name must be between 1 and 100 characters')
        return value

    @validates('ingredients')
    def validate_ingredients(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError('ingredients must be present')
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, value):
        if value is None:
            raise ValueError('price must be present')
        try:
            v = float(value)
        except (ValueError, TypeError):
            raise ValueError('price must be a valid number')
        if v < 0 or v > 30:
            raise ValueError('price must be between 0 and 30')
        return v

    def to_dict(self, include_restaurant=False, include_pizza=True):
        base = {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id
        }
        if include_restaurant:
            base['restaurant'] = self.restaurant.to_dict(include_pizzas=False)
        if include_pizza:
            base['pizza'] = self.pizza.to_dict()
        return base
