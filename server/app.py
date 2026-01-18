#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# ========================
# Index route
# ========================
@app.route('/')
def index():
    return '<h1>Bakery API</h1>'

# ========================
# GET routes
# ========================
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries])

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict(rules=('-created_at', '-updated_at')))

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([bg.to_dict() for bg in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(baked_good.to_dict())

# ========================
# POST route
# ========================
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    new_baked_good = BakedGood(
        name=name,
        price=price,
        bakery_id=bakery_id
    )
    db.session.add(new_baked_good)
    db.session.commit()

    return jsonify(new_baked_good.to_dict()), 201

# ========================
# PATCH route
# ========================
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    new_name = request.form.get('name')
    if new_name:
        bakery.name = new_name
        db.session.commit()

    return jsonify(bakery.to_dict())

# ========================
# DELETE route
# ========================
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({"message": "Baked good deleted successfully"})

# ========================
# Run the app
# ========================
if __name__ == '__main__':
    app.run(port=5555, debug=True)
