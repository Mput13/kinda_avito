# import flask
# from flask import jsonify, request
#
# from data import db_session
# from data.users import User
#
# blueprint = flask.Blueprint(
#     'users_api',
#     __name__,
#     template_folder='templates'
# )
#
#
# @blueprint.route('/api/users/create_user', methods=['POST'])
# def create_user():
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in request.json for key in
#                  ['login', 'hashed_password']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     new_user = User()
#     new_user.login = request.json['login']
#     new_user.hashed_password = request.json['hashed_password']
#     db_sess.add(new_user)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
