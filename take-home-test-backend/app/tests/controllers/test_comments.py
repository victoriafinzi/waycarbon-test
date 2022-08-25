import unittest

from app import create_app
from app.tests import TestConfig, create_tables


class CommentsControllerTest(unittest.TestCase):
    def setUp(self):
        # setup a test application using an in-memory database
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
