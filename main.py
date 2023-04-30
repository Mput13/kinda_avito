import uuid

from flask import Flask, request, send_file
from flask_restful import Api

import image_restful
from data import db_session
from data.files import File
from data.images import Image
from routes import lots_restful, users_restful, categories_restful

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


@app.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files['file']
    saving_name = f'./images/{uuid.uuid4()}.upload'
    file.save(saving_name)
    session = db_session.create_session()
    new_file = File()
    new_file.path = saving_name
    session.add(new_file)
    session.commit()

    return {'id': new_file.id}


@app.route('/get-image', methods=['GET'])
def get_image():
    args = request.args.to_dict()
    session = db_session.create_session()
    image = session.query(Image).where(Image.id == int(args['image_id'])).all()
    if int(args['image_id']) == -1:
        return send_file('./images/amonga.png')
    else:
        return send_file(image[0].path)


if __name__ == "__main__":
    main()
