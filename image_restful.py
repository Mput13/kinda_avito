import io
from base64 import b64decode as dec64
from base64 import encodebytes

from PIL import Image
from flask import abort, jsonify, request
from flask_restful import reqparse, Resource

from data import db_session
from data.categories import Category
from data.images import Image


def abort_if_news_not_found(id):
    session = db_session.create_session()
    images = session.query(Category).get(id)
    if not images:
        abort(404, message=f"Image {id} not found")


def get_bite_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


class ImageResource(Resource):
    def get(self, id):
        abort_if_news_not_found(id)
        session = db_session.create_session()
        images = session.query(Image).where(Image.lot_id == id)
        encoded_imges = []
        for image in images:
            encoded_imges.append(get_bite_image(image.path))
        return jsonify({'photos': encoded_imges})

    def delete(self, id):
        abort_if_news_not_found(id)
        session = db_session.create_session()
        image = session.query(Category).get(id)
        session.delete(image)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('path', required=True)
parser.add_argument('lot_id', type=int, required=True)


class ImageListResource(Resource):
    # def get(self):
    #     session = db_session.create_session()
    #     news = session.query(Category).all()
    #     return jsonify({'': [item.to_dict(
    #         only=('id', 'category')) for item in news]})

    def post(self):
        args = parser.parse_args()
        # data = request.data.decode('utf-8')
        # print(data)
        files = request.files['files']
        session = db_session.create_session()
        image = Image()
        image.path = args['path']
        # for i, file in enumerate(files):
        #     Image.open(io.BytesIO(dec64(file))).save(args['path'])
        Image.open(io.BytesIO(dec64(file))).save(args['path'])
        image.lot_id = args['lot_id']
        session.add(image)
        session.commit()
        return jsonify({'success': 'OK'})
