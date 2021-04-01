# wsgi.py
# pylint: disable=missing-docstring

BASE_URL = '/api/v1'

from flask import Flask, abort, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
from models import Product
from schemas import many_product_schema
from schemas import one_product_schema

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products', methods=['POST'])
def post_one_product():
    content = request.get_json()
    if content is None:
        abort(400)

    product = Product()
    product.name = content['name']
    db.session.add(product)
    db.session.commit()
    return one_product_schema.jsonify(product), 201

@app.route(f'{BASE_URL}/products/<int:id>', methods=['DELETE'])
def delete_one_product(id):
    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)

    db.session.delete(product)
    db.session.commit()
    return "", 204

@app.route(f'{BASE_URL}/products/<int:id>', methods=['PATCH'])
def update_one_product(id):
    content = request.get_json()
    if content is None:
        abort(400)

    product = db.session.query(Product).get(id)
    if product is None:
        abort(422)

    product.name = content['name']
    db.session.commit()
    return "", 204


@app.route(f'{BASE_URL}/products/<int:id>', methods=['GET'])
def read_one_product(id):
    content = request.get_json()
    if content is None:
        abort(400)

    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)
    return one_product_schema.jsonify(product), 200


