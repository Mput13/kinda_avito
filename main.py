from flask import Flask
from flask_restful import Api

from data import db_session
from routes import lots_api, users_api, lots_restful, users_restful

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'asdfasdfasdfsf'

# login_manager.init_app(app)
#
api.add_resource(lots_restful.LotListResource, '/api/v2/lots')
api.add_resource(lots_restful.LotResource, '/api/v2/lots/<int:id>')

api.add_resource(users_restful.UserListResource, '/api/v2/users')
api.add_resource(users_restful.UserResource, '/api/v2/users/<int:id>')

def main():
    db_session.global_init("db/blogs.db")
    app.run(host='0.0.0.0', port=8005, debug=True)


if __name__ == "__main__":
    main()
