from werkzeug.exceptions import NotFound
import unittest

from app import create_app, db, Flask
from app.repositories.models import User, Post, Comment
from app.controllers.posts import get_all_posts, get_post_by_id
from app.tests import TestConfig, create_tables


class PostsControllerTest(unittest.TestCase):
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
            content="This is the post's text.",
            comments=[
                Comment(user=user_b, content="This is a comment.")
            ]
        )

        self.another_test_post = Post(
            user=user_b,
            title="Another post's title",
            content="This is the post's text"
        )

        db.session.add_all([self.test_post, self.another_test_post])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_posts(self):
        """ Should return all posts in a valid format"""
        res = get_all_posts()
        self.assertIsNotNone(res)
        self.assertIsInstance(res, Flask.response_class)
        self.assertEqual(200, res.status_code)

    def test_get_post_by_id(self):
        """ Should return a posts by It`s id in a valid format"""
        res = get_post_by_id(self.test_post.id)
        self.assertIsNotNone(res)
        self.assertIsInstance(res, Flask.response_class)
        self.assertEqual(200, res.status_code)
