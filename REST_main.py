from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    map_url = db.Column(db.String(240), nullable=False)
    img_url = db.Column(db.String(240), nullable=False)
    location = db.Column(db.String(240), nullable=False)
    has_sockets = db.Column(db.Boolean, default=True)
    has_toilet = db.Column(db.Boolean, default=True)
    can_take_calls = db.Column(db.Boolean, default=True)
    seats = db.Column(db.String(240), nullable=False)
    coffee_price = db.Column(db.String(240), nullable=False)
    has_wifi = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'map_url': self.map_url,
            'img_url': self.img_url,
            'location': self.location,
            'has_sockets': self.has_sockets,
            'has_toilet': self.has_toilet,
            'can_take_calls': self.can_take_calls,
            'seats': self.seats,
            'coffee_price': self.coffee_price

        }


@app.route('/')
def get_all_cafe():
    random_cafe = db.session.execute(db.select(Cafe).order_by(db.sql.func.random()).limit(1)).scalar()
    print(random_cafe)
    return jsonify(Cafe={
        'id': random_cafe.id,
        'name': random_cafe.name,
        'map_url': random_cafe.map_url,
        'img_url': random_cafe.img_url,
        'location': random_cafe.location,
        'has_sockets': random_cafe.has_sockets,
        'has_toilet': random_cafe.has_toilet,
        'can_take_calls': random_cafe.can_take_calls,
        'seats': random_cafe.seats,
        'coffee_price': random_cafe.coffee_price
    })


@app.route('/all_cafe', methods=['GET'])
def all_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route('/search_url', methods=['GET'])
def search_url():
    cafe_name = request.args.get('name')

    result = db.session.execute(db.select(Cafe).where(Cafe.location == cafe_name))
    found_cafe = result.scalar()

    cafe_data = found_cafe.to_dict()
    return jsonify(cafe=cafe_data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        cafe_name = request.form['cafe_name']
        result1 = db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name))
        found_cafe1 = result1.scalar().all()

        cafe_data1 = found_cafe1.to_dict()
        return jsonify(cafe=cafe_data1)
    return render_template("search.html")


@app.route('/add', methods=['POST'])
def add():
    name = request.args.get('name')
    location = request.args.get('location')
    map = request.args.get('map')
    img = request.args.get('img')
    seats = request.args.get('seats')
    coffee_price = request.args.get('coffee_price')
    new_cafe = Cafe(name=name, location=location, map_url=map, img_url=img, seats=seats, coffee_price=coffee_price)
    db.session.add(new_cafe)
    db.session.commit()
    return "NEW DATA ADDED SUCCESSFULLY"


@app.route('/update', methods=['PATCH'])
def update():
    cafe_id = request.args.get('cafe_id')
    new_name = request.args.get('name')
    new_location = request.args.get('location')
    new_map = request.args.get('map')
    new_img = request.args.get('img')
    new_seats = request.args.get('seats')
    new_coffee_price = request.args.get('coffee_price')

    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify(error=f"Cafe with ID {cafe_id} not found"), 404
    else:
        if new_name:
            cafe.name = new_name
        if new_location:
            cafe.location = new_location
        if new_map:
            cafe.map_url = new_map
        if new_img:
            cafe.img_url = new_img
        if new_seats:
            cafe.seats = new_seats
        if new_coffee_price:
            cafe.coffee_price = new_coffee_price
        db.session.commit()
    return "Updated successful"


if __name__ == '__main__':
    app.run(debug=True, port=5010)
