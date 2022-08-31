from unittest import result
from flask import Flask
import datetime
import json
from typing import Dict
import unittest
from xml.dom import NotFoundErr
from xml.etree.ElementTree import Comment

from app import create_app, db
from app.repositories import comments
from app.controllers.comments.utils import _comment_to_dict, add_children
from app.repositories.models import Post, User, Comment
from app.tests import TestConfig, create_tables
from app.controllers.comments import get_coment_tree_by_user_id, get_comments_from_post, get_comment_by_id


class CommentsControllerTest(unittest.TestCase):
    def setUp(self):
        # setup a test application using an in-memory database
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables(db)


        # insert a few entities in the db
        user_a = User(username="User A")
        user_b = User(username="User B")
        user_c = User(username="User C")

        self.test_post = Post(
            user=user_a,
            title="Some title",
            content="This is the post content.",
            comments=[
                Comment(user=user_b, content="This is a comment."),
                Comment(user=user_c, content="This is another coment.")
            ]
        )

        db.session.add(self.test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_add_children(self):
        """ Should add children comments to a root comment from a post """
        resp = [{'id': 1, 'timestamp': datetime.datetime(2022, 8, 28, 16, 40, 4), 'author': {'id': 1, 'name': 'Joao'}, 'post': {'id': 1, 'title': 'Teste.'}, 'content': 'aaa', 'children': []}]
        list_comments = [{'id': 2, 'timestamp': datetime.datetime(2022, 8, 30, 13, 24, 38), 'author': {'id': 2, 'name': 'Maria'}, 'post': {'id': 1, 'title': 'Teste.'}, 'content': 'bbb', 'parent': {'id': 1, 'author': 'Joao', 'content': 'aaa'}}]
        add_children(resp, list_comments)
        self.assertTrue(resp[0]['children'] != None)


    def test_get_comment_by_id(self):
        """ Should have a valid return """
        comment = get_comment_by_id(1)
        self.assertIsInstance(comment, Flask.response_class)
        self.assertTrue(comment is not None)
        self.assertEqual(200, comment.status_code)


    def test_get_comments_from_post_success(self):
        """ Should return all comments by the id of a post """
        all_comments = get_comments_from_post(1)
        self.assertIsInstance(all_comments, Flask.response_class)
        self.assertTrue(all_comments is not None)
        self.assertEqual(200, all_comments.status_code)


    def test_comment_to_dict(self):
        """ Should transform a comment to a dict """
        comment = _comment_to_dict(comments.get_comment_by_id(1))
        self.assertTrue(comment is not None)
        self.assertIsInstance(comment, dict)


    def test_get_coment_tree_by_user_id(self):
        """ Should return all comments by the id of a post """
        all_comments = get_coment_tree_by_user_id(1)
        self.assertIsInstance(all_comments, Flask.response_class)
        self.assertTrue(all_comments is not None)
        self.assertEqual(200, all_comments.status_code)
