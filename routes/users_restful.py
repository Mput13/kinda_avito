from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import select

from data import db_session
from data.users import User


def abort_if_user_not_found(id):
    session = db_session.create_session()
    user = session.query(User).get(id)
    session.close()
    if not user:
        abort(404, message=f"News {id} not found")


class UserResource(Resource):
    def get(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        lot = session.query(User).get(id)
        session.close()
        return jsonify({'user': lot.to_dict(
            only=('id', 'telegram_id', 'created_date'))})

    def delete(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('telegram_id', required=True)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        session.close()
        return jsonify({'users': [item.to_dict(
            only=('id', 'telegram_id', 'created_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.scalar(select(User).where(User.telegram_id == args['telegram_id']))
        if not user:
            user = User()
            user.telegram_id = args['telegram_id']
            session.add(user)
            session.commit()
            session.close()
            return jsonify({'success': 'OK'})
        else:
            session.close()
            return jsonify({'такой уже есть': 'OK'})