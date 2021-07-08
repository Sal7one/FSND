import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

# Custom database setup because compatibility issues with windows
        self.database_name = "trivia_test"
        self.PORT = 5432
        self.DB_USERNAME = 'student'
        self.DB_PATH = 'localhost'
        self.database_path = f'postgresql://{self.DB_USERNAME}:aa050@{self.DB_PATH}:{self.PORT}/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_questions(self):
        response = self.client().get('/questions/')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(res['questions'])
        self.assertTrue(res['total_questions'])
        self.assertTrue(res['categories'])

     # Post is not allowed at this endpoint so method not allowed (405) is excpted
    def test_405_retrieve_questions(self):
        response = self.client().post('/questions/')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(res['error'], 405)

    def test_questions_by_category(self):
        response = self.client().get('/categories/2')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['currentCategory'], 'Art')
        self.assertTrue(res['questions'])
        self.assertTrue(res['total_questions'])

    def test_500_questions_by_category(self):
        response = self.client().get('/categories/20202021')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 500)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
