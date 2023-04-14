from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.users import User


def abort_if_user_not_found(lot_id):
    session = db_session.create_session()
    user = session.query(User).get(lot_id)
    if not user:
        abort(404, message=f"News {lot_id} not found")


class UserResource(Resource):
    def get(self, lot_id):
        abort_if_user_not_found(lot_id)
        session = db_session.create_session()
        lot = session.query(User).get(lot_id)
        return jsonify({'user': lot.to_dict(
            only=('id', 'telegram_id', 'created_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('telegram_id', required=True)
parser.add_argument('id', type=int)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'telegram_id', 'created_date')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.telegram_id = args['telegram_id']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})