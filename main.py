from flask import Flask
from flask_restful import Api

from data import db_session
from routes import lots_api

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'asdfasdfasdfsf'


# login_manager.init_app(app)
#
# api.add_resource(news_restful.NewsResource)
# api.add_resource(news_restful.NewsListResource)

def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(lots_api.blueprint)
    app.run()


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='0.0.0.0', port=8005, debug=True)


if __name__ == "__main__":
    main()
