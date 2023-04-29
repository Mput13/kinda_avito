from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from sqlalchemy import select

from data import db_session
from data.categories import Category
from data.lots import Lot


def abort_if_lot_not_found(id):
    session = db_session.create_session()
    lot = session.query(Lot).get(id)
    if not lot:
        abort(404, message=f"Lot {id} not found")


class LotResource(Resource):
    def get(self, id):
        abort_if_lot_not_found(id)
        session = db_session.create_session()
        lot = session.scalar(select(Lot).where(Lot.id == id))
        session.close()
        return jsonify({'lot': lot.to_dict(
            only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator'))})

    def delete(self, id):
        args = request.args.to_dict()
        abort_if_lot_not_found(id)
        session = db_session.create_session()
        lot = session.query(Lot).get(id)
        if lot.creator == args['user']:
            session.delete(lot)
            session.commit()
            session.close()
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'failed': 'Вы не создатель объявления'})


parser = reqparse.RequestParser()
# parser.add_argument('id', type=int)
parser.add_argument('title', required=True)
parser.add_argument('price', required=True, type=float)
parser.add_argument('description')
parser.add_argument('category')
parser.add_argument('creator', required=True)


class LotListResource(Resource):
    def get(self):
        args = request.args.to_dict()
        session = db_session.create_session()
        if args.get('category'):
            lots = session.query(Lot).where(Lot.category == args.get('category') and Lot.creator == args.get('watcher'))
        elif len(args.keys()) == 0:
            lots = session.query(Lot).all()
        elif bool(args.get('user_lots')):
            lots = session.query(Lot).where(Lot.creator == args.get('watcher'))
        else:
            lots = session.query(Lot).where(Lot.creator != args.get('watcher'))
        session.close()
        return jsonify({'lots': [item.to_dict(
            only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator')) for item in lots]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lot = Lot()
        lot.title = args['title']
        # if session.scalar(select(Lot).where(Lot.title == args['title'])):
        #     return jsonify({'Error': f'Lot with title {args["title"]} already exists'})
        lot.price = args['price']
        lot.description = args['description']
        lot.category = args['category']
        category = Category()
        category.category = args['category']
        ctgr = session.scalar(select(Category).where(Category.category == args['category']))
        lot.creator = args['creator']
        session.add(lot)
        if not ctgr:
            session.add(category)
        session.commit()
        return jsonify({'success': 'OK',
                        'id': lot.id})
