'''
Уникальный идентификатор пользователя — некоторый его номер в нашей базе данных, желательно, чтобы он генерировался автоматически без нашего участия.
Имя пользователя — некоторое строковое значение.
Описание пользователя — некоторая текстовая информация, которой пользователь хочет поделиться о себе.
Адрес электронной почты — уникальная строка (чтобы мы могли точно знать, для какого пользователя восстанавливать пароль). Так как мы достаточно часто будем искать пользователя по адресу электронной почты (как минимум, при логине), было бы здорово, если бы база могла как-то ускорить такой поиск.
Зашифрованный пароль пользователя — строка. Ни в коем случае нельзя хранить пароль пользователя в открытом виде!
Дата создания пользователя — потому что нам хочется знать, когда пользователь зарегистрировался в нашем веб-приложении.
'''

import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    jobs = orm.relation("Jobs", back_populates='user')

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"
