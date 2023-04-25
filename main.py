import pprint

from flask import Flask, request, jsonify
from flask_restful import Api
from sqlalchemy import select, and_

import image_restful
from data import db_session
from data.lots import Lot
from routes import lots_api, users_api, lots_restful, users_restful, categories_restful

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'asdfasdfasdfsf'

# login_manager.init_app(app)
#
api.add_resource(lots_restful.LotListResource, '/api/v2/lots')
api.add_resource(lots_restful.LotResource, '/api/v2/lots/<int:id>')

api.add_resource(users_restful.UserListResource, '/api/v2/users')
api.add_resource(users_restful.UserResource, '/api/v2/users/<int:id>')

api.add_resource(categories_restful.CategoryListResource, '/api/v2/categories')
api.add_resource(categories_restful.CategoryResource, '/api/v2/categories/<int:id>')

api.add_resource(image_restful.ImageListResource, '/api/v2/images')
api.add_resource(image_restful.ImageResource, '/api/v2/images/<int:id>')


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='0.0.0.0', port=8005, debug=True)


# @app.route('/api/v2/lots/search', methods=['GET'])
# def search():
#     # В разработке
#     args = request.args.to_dict()
#     if args.get('')
#     session = db_session.create_session()
#     stmt = select(Lot().where(Lot.creator == args.get('creator')))
#     output = [item.to_dict(only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator'))
#               for item in session.scalars(stmt)]
#     return jsonify(output)


if __name__ == "__main__":
    main()
