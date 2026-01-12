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
 