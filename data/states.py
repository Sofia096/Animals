import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class States(SqlAlchemyBase):
    __tablename__ = 'states'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tag = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')