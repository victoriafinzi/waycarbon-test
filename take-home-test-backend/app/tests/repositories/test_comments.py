import unittest

import app.repositories.comments as CommentsRepository

from app.repositories.models import User, Post, Comment
from app import create_app, db
from app.tests import TestConfig, create_tables


class CommentsRepositoryTest(unittest.TestCase):
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

    def test_get_existing_comment_by_id(self):
        """ Should return a comment correctly when it exists. """
        test_comment = self.test_post.comments[0]
        result = CommentsRepository.get_comment_by_id(test_comment.id)

        # the return value should be an instance of Comment
        self.assertIsInstance(result, Comment)

        # the return value should be a comment with the same id as passed to the
        # function.
        self.assertEqual(result.id, test_comment.id)

    def test_get_nonexisting_comment_by_id(self):
        """ Should return None when the referenced comment does not exist. """
        non_existing_comment_id = 0
        retrieved_comment = CommentsRepository.get_comment_by_id(
            non_existing_comment_id)

        # the return value should be None
        self.assertIsNone(retrieved_comment)

    def test_get_existing_post_comments(self):
        """ Should return all comments from an existing post """
        result = CommentsRepository.get_post_comments(self.test_post.id)

        # the return value should be a list
        self.assertIsInstance(result, list)

        # each element of the return list should be an instance of Comment
        self.assertTrue(
            all(isinstance(comment, Comment) for comment in result)
        )

        # the list should have the same number of elements as the post has
        # comments.
        post_comments = list(self.test_post.comments)
        self.assertEqual(len(result), len(post_comments))

        # all the post's comments should be present in the return list.
        returned_ids = sorted(comment.id for comment in result)
        post_comment_ids = sorted(comment.id for comment in post_comments)
        self.assertEqual(returned_ids, post_comment_ids)

    def test_get_nonexisting_post_comments(self):
        """ Should return an empty list when the referenced post does not exist.
        """
        non_existing_post_id = 0
        result = CommentsRepository.get_post_comments(non_existing_post_id)

        # the return value should be a list
        self.assertIsInstance(result, list)

        # the return list should be empty
        self.assertEqual(len(result), 0)
