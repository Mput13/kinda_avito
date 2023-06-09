import datetime
from typing import Any

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    telegram_id: Column[Any] = sqlalchemy.Column(sqlalchemy.String,
                                    index=True, unique=True)
    # hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    lot = orm.relationship("Lot", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
