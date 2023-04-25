import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Lot(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lots'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Float)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    creator = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("users.telegram_id"))
    user = orm.relationship('User')
    category_rel = orm.relationship("Category", back_populates='lot')
    image = orm.relationship("Image", back_populates='lot')