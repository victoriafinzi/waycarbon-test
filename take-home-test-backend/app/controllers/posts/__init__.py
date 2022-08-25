from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify

from app.repositories import posts
from .utils import _post_to_dict

BLUEPRINT = Blueprint('posts', __name__)


@BLUEPRINT.route('/posts')
def get_all_posts():
    return jsonify([
        _post_to_dict(post)
        for post in posts.get_all_posts()
    ])


@BLUEPRINT.route('/posts/<post_id>')
def get_post_by_id(post_id):
    post = posts.get_post_by_id(post_id)

    if post is None:
        raise NotFound()

    return jsonify(_post_to_dict(post, with_content=True))
