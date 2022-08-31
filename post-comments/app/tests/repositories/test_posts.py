import unittest

import app.repositories.posts as PostsRepository

from app.repositories.models import User, Post, Comment
from app import create_app, db
from app.tests import TestConfig, create_tables


class PostsRepositoryTest(unittest.TestCase):
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

    def test_get_existing_post_by_id(self):
        """ Should return a post correctly when it exists """
        result = PostsRepository.get_post_by_id(self.test_post.id)

        # result should be an instance of Post
        self.assertIsInstance(result, Post)

        # the returned post should have the same id as was passed to the
        # function.
        self.assertEqual(result.id, self.test_post.id)

    def test_get_nonexisting_post_by_id(self):
        """ Should return None when trying to get a non-existing post """
        non_existing_post_id = 0
        result = PostsRepository.get_post_by_id(non_existing_post_id)

        # return value should be None
        self.assertIsNone(result)

    def test_get_all_posts(self):
        """ Should return a list with all the posts in the database """
        result = PostsRepository.get_all_posts()

        # result should be a list
        self.assertIsInstance(result, list)

        # every element in the return list should be an instance of Post
        self.assertTrue(
            all(isinstance(post, Post) for post in result)
        )

        # as we only inserted two posts in the db, both should be in the return
        # list.
        inserted_post_ids = sorted(
            [self.test_post.id, self.another_test_post.id])
        returned_post_ids = sorted(post.id for post in result)
        self.assertEqual(inserted_post_ids, returned_post_ids)
