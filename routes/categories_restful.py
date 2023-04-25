from flask import abort, jsonify
from flask_restful import reqparse, Resource

from data import db_session
from data.categories import Category


def abort_if_news_not_found(id):
    session = db_session.create_session()
    categoies = session.query(Category).get(id)
    if not categoies:
        abort(404, message=f"Category {id} not found")


class CategoryResource(Resource):
    def get(self, id):
        abort_if_news_not_found(id)
        session = db_session.create_session()
        news = session.query(Category).get(id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, id):
        abort_if_news_not_found(id)
        session = db_session.create_session()
        news = session.query(Category).get(id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('category', required=True)


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Category).all()
        return jsonify({'categories': [item.to_dict(
            only=('id', 'category')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category()
        category.category = args['category']
        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})
