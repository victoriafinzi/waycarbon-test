from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

from app.repositories.models import User, Post, Comment


class TestConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///'  # in-memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_tables(db: SQLAlchemy) -> None:
    """ Create or re-create tables if they already exist """
    def drop_and_create(model: db.Model) -> None:
        try:
            model.__table__.drop(db.engine)
        except OperationalError:
            pass
        finally:
            model.metadata.create_all(db.engine)

    drop_and_create(User)
    drop_and_create(Post)
    drop_and_create(Comment)
