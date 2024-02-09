from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/drinks/<tastes_like_grapes>')
def get_drinks(tastes_like_grapes):
    drinks = Drink.query.filter_by(description=tastes_like_grapes).all()
    drink_list = [{"name": drink.name, "description": drink.description} for drink in drinks]
    return jsonify({"drinks": drink_list})

@app.route('/add_drink', methods=['POST'])
def add_drink():
    data = request.get_json()

    if 'name' not in data or 'description' not in data:
        return jsonify({"error": "Missing 'name' or 'description' in request body"}),

    new_drink = Drink(name=data['name'], description=data['description'])
    db.session.add(new_drink)
    db.session.commit()

    return jsonify({"message": "Drink added successfully"}),

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        initial_drinks = [
            Drink(name='Cola', description='Classic flavor'),
            Drink(name='fanta', description='Fresh orange juice'),
            Drink(name='Water', description='refreshing water')
        ]

        db.session.add_all(initial_drinks)
        db.session.commit()

    app.run(debug=True)



