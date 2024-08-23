#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

        new_good = BakedGood(
            name = request.form.get('name'),
            price = request.form.get('price')
        )

        db.session.add(new_good)
        db.session.commit()

        response = make_response(
            jsonify(new_good.to_dict()),
            201
        )
        return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_goods(id):

        good = BakedGood.query.filter_by(id=id).first()

        db.session.delete(good)
        db.session.commit()

        response = make_response(
            jsonify(
                 {
                      "delete_successful" : True,
                      "message" : "baked_good deleted"
                      }
            ),
            200
        )
        return response

@app.route('/bakeries/<int:id>', methods=['GET','PATCH'])
def bakery_by_id(id):

    if request.method == 'GET':
        bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()
        return make_response ( bakery_serialized, 200  )
    
    elif request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()

        for attr in request.form:
            setattr(bakery, attr, request.form[attr])

            db.session.add(bakery)
            db.session.commit()

        response = make_response(
            jsonify(bakery.to_dict()),
            200
        )
        return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)