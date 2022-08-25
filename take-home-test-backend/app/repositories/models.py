from sqlalchemy import func, select
from sqlalchemy.orm import column_property
from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, nullable=False)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='comments', lazy='joined')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    parent_comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comments.id'),
        nullable=True)

    # NOTE: 'children' is just a utility property, used only for populating
    # the database. It lazy-loads the association on access and *will*
    # result in uneeded database queries (especially in recursive contexts).
    #
    # Don't use it!
    children = db.relationship(
        'Comment',
        backref=db.backref('parent_comment', remote_side=[id]))

    created_at = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
        nullable=False)

    content = db.Column(db.String, nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts', lazy='joined')

    created_at = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
        nullable=False)

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    num_comments = column_property(
        select([func.count(Comment.id)])
            .where(Comment.post_id == id)
            .scalar_subquery()
    )