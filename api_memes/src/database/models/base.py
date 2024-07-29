import sqlalchemy

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True
    )