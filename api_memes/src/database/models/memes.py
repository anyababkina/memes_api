import sqlalchemy

from src.database.models.base import Base


class Memes(Base):
    __tablename__ = 'memes'

    description = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )

