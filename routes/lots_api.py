# import flask
# from flask import jsonify, request
# from sqlalchemy import select
#
# from data import db_session
# from data.lots import Lot
# from data.users import User
#
# blueprint = flask.Blueprint(
#     'users_api',
#     __name__,
#     template_folder='templates'
# )
#
#
# @blueprint.route('/api/lots/create_lot', methods=['POST'])
# def create_lot():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['login', 'hashed_password']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     new_lot = Lot()
#     new_lot.title = request.json['title']
#     new_lot.price = request.json['price']
#     new_lot.description = request.json['description']
#     new_lot.category = request.json['category']
#     new_lot.creator = request.json['creator']
#     db_sess.add(new_lot)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
#
# @blueprint.route('/api/lots/get_all_lots', methods=['GET'])
# def get_all_lots():
#     stmt = select(Lot)
#     output = [item.to_dict(only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator'))
#               for item in db_session.scalars(stmt)]
#     return jsonify(output)
#
#
# @blueprint.route('/api/lots/', methods=['GET'])
# def get_all_lots():
#     stmt = select(Lot)
#     output = [item.to_dict(only=('id', 'title', 'price', 'description', 'category', 'created_date', 'creator'))
#               for item in db_session.scalars(stmt)]
#     return jsonify(output)
#
#
# @blueprint.route('/api/lots/change_lot', methods=['POST'])
# def change_lot():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['login', 'hashed_password']):
#         return jsonify({'error': 'Bad request'})
#     pass
#     return jsonify({'success': 'OK'})
