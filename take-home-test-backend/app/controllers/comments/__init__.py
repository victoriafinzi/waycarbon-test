from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify

from app.repositories import comments

from .utils import _comment_to_dict

BLUEPRINT = Blueprint('comments', __name__)


@BLUEPRINT.route('/comments/<comment_id>')
def get_comment_by_id(comment_id):
    comment = comments.get_comment_by_id(comment_id)

    if comment is None:
        raise NotFound

    return jsonify(_comment_to_dict(comment))


@BLUEPRINT.route('/posts/<post_id>/comments')
def get_comments_from_post(post_id):
    return jsonify([
        _comment_to_dict(comment)
        for comment in comments.get_post_comments(post_id)
    ])

