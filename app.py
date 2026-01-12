from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Episode, Guest, Appearance

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        episodes = Episode.query.all()
        return jsonify([e.to_dict(fields=('id','date','number')) for e in episodes])

    @app.route('/episodes/<int:ep_id>', methods=['GET'])
    def get_episode(ep_id):
        ep = Episode.query.get(ep_id)
        if not ep:
            return jsonify({"error": "Episode not found"}), 404
        return jsonify(ep.to_dict(include_appearances=True))

    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()
        return jsonify([g.to_dict(fields=('id','name','occupation')) for g in guests])

    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        data = request.get_json() or {}
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')

        errors = []
        if rating is None:
            errors.append('rating is required')
        if episode_id is None:
            errors.append('episode_id is required')
        if guest_id is None:
            errors.append('guest_id is required')

        if errors:
            return jsonify({"errors": errors}), 400

        # Ensure episode and guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        if not episode or not guest:
            return jsonify({"errors": ["episode or guest not found"]}), 400

        appearance = Appearance(rating=rating, episode=episode, guest=guest)
        try:
            db.session.add(appearance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

        return jsonify(appearance.to_dict(include_episode=True, include_guest=True)), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    