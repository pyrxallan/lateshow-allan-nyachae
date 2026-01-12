from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Episode, Guest, Appearance, Restaurant, Pizza, RestaurantPizza

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
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

    # Restaurant routes
    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([r.to_dict() for r in restaurants])

    @app.route('/restaurants', methods=['POST'])
    def create_restaurant():
        data = request.get_json() or {}
        name = data.get('name')
        address = data.get('address')

        errors = []
        if not name:
            errors.append('name is required')
        if not address:
            errors.append('address is required')

        if errors:
            return jsonify({"errors": errors}), 400

        try:
            restaurant = Restaurant(name=name, address=address)
            db.session.add(restaurant)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

        return jsonify(restaurant.to_dict()), 201

    @app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
    def get_restaurant(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        return jsonify(restaurant.to_dict(include_pizzas=True))

    @app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
    def delete_restaurant(restaurant_id):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        try:
            db.session.delete(restaurant)
            db.session.commit()
            return jsonify({"message": "Restaurant deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Pizza routes
    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify([p.to_dict() for p in pizzas])

    @app.route('/pizzas', methods=['POST'])
    def create_pizza():
        data = request.get_json() or {}
        name = data.get('name')
        ingredients = data.get('ingredients')

        errors = []
        if not name:
            errors.append('name is required')
        if not ingredients:
            errors.append('ingredients is required')

        if errors:
            return jsonify({"errors": errors}), 400

        try:
            pizza = Pizza(name=name, ingredients=ingredients)
            db.session.add(pizza)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

        return jsonify(pizza.to_dict()), 201

    # RestaurantPizza routes
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.get_json() or {}
        price = data.get('price')
        restaurant_id = data.get('restaurant_id')
        pizza_id = data.get('pizza_id')

        errors = []
        if price is None:
            errors.append('price is required')
        if restaurant_id is None:
            errors.append('restaurant_id is required')
        if pizza_id is None:
            errors.append('pizza_id is required')

        if errors:
            return jsonify({"errors": errors}), 400

        # Ensure restaurant and pizza exist
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)
        if not restaurant or not pizza:
            return jsonify({"errors": ["restaurant or pizza not found"]}), 400

        try:
            restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
            db.session.add(restaurant_pizza)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400

        return jsonify(restaurant_pizza.to_dict(include_restaurant=True, include_pizza=True)), 201

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    