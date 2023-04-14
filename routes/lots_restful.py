from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.lots import Lot


def abort_if_lot_not_found(lot_id):
    session = db_session.create_session()
    lot = session.query(Lot).get(lot_id)
    if not lot:
        abort(404, message=f"Lot {lot_id} not found")


class LotResource(Resource):
    def get(self, lot_id):
        abort_if_lot_not_found(lot_id)
        session = db_session.create_session()
        lot = session.query(Lot).get(lot_id)
        return jsonify({'lot': lot.to_dict(
            only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator'))})

    def delete(self, id):
        abort_if_lot_not_found(id)
        session = db_session.create_session()
        lot = session.query(Lot).get(id)
        session.delete(lot)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
# parser.add_argument('id', type=int)
parser.add_argument('title', required=True)
parser.add_argument('price', required=True, type=float)
parser.add_argument('description')
parser.add_argument('category')
parser.add_argument('creator', required=True)


class LotListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Lot).all()
        return jsonify({'lots': [item.to_dict(
            only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lot = Lot()
        lot.title = args['title']
        lot.price = args['price']
        lot.description = args['description']
        lot.category = args['category']
        lot.creator = args['creator']
        session.add(lot)
        session.commit()
        return jsonify({'success': 'OK'})
