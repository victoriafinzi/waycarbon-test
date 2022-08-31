import json
import sys
from urllib import response
from werkzeug.exceptions import NotFound
from flask import Blueprint, jsonify

from app.repositories import comments

from .utils import _comment_to_dict, add_children

BLUEPRINT = Blueprint('comments', __name__)


@BLUEPRINT.route('/comments/<comment_id>')
def get_comment_by_id(comment_id):
    comment = comments.get_comment_by_id(comment_id)

    if comment is None:
        raise NotFound

    return jsonify(_comment_to_dict(comment))


@BLUEPRINT.route('/posts/<post_id>/comments')
def get_comments_from_post(post_id):
    nested_comments_list = [] 
    list_comments = [] 
    all_comments = comments.get_post_comments(post_id) 
    try:
        for comment in all_comments: 
            list_comments.append(_comment_to_dict(comment)) 
        for comment in list(list_comments): 
            if comment["parent"] is None:
                del comment["parent"]
                comment["children"] = [] 
                nested_comments_list.append(comment) 
                list_comments.remove(comment) 
        add_children(nested_comments_list, list_comments) 
        print(type(jsonify(nested_comments_list)))
        return jsonify(200, nested_comments_list)
    except AttributeError:
        return (404, 'Comment not found')
    except:
        return (500, 'Internal server error')


@BLUEPRINT.route('/users/<user_id>/comments')
def get_coment_tree_by_user_id(user_id):
    """ 
        The function is not completed 
        Runned out of time to finish it
    """
    comment_by_user = comments.get_comment_by_user_id(user_id)
    list_comments = [] 
    nested_comments_list = []
    for comment in comment_by_user: 
        list_comments.append(_comment_to_dict(comment))
    # for comment in list(list_comments): 
    #     if comment["parent"] is None:
    #         del comment["parent"]
    #         comment["children"] = [] 
    #         nested_comments_list.append(comment) 
    #         list_comments.remove(comment) 
    # add_children(nested_comments_list, list_comments)   
    return jsonify(200, list_comments)

"""
Roots Natalie -> parent 
"""