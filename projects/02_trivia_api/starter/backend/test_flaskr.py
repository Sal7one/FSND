import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import random

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
        self.database_path = f'postgresql://{self.DB_USERNAME}@{self.DB_PATH}:{self.PORT}/{self.database_name}'
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

    # ------------- TEST 0  ---------------------------
    # Random endpoint

    def test_none_exsisting_endpoint(self):
        response = self.client().get('/radnom_end_point')
        self.assertEqual(response.status_code, 404)

    # ------------- TEST 1  ------ Correct request ---------------------

    # Get question function / endpoint
    def test_retrieve_questions(self):
        response = self.client().get('/questions/')
        res = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        # Udacity requirements:  Should see questions and categories generated
        self.assertTrue(res['questions'])
        self.assertTrue(res['categories'])
        self.assertTrue(res['total_questions'])

        # Udacity requirements:
        # Ten questions per page
        self.assertEqual(len(res['questions']), 10)

    # ------------- TEST 1  ------ Bad request ---------------------
    # Post is not allowed at this endpoint so method not allowed (405)

    def test_retrieve_questions(self):
        response = self.client().post('/questions/')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(res['error'], 405)

    # ------------- TEST 2  ------ Correct request ---------------------
    def test_questions_by_category(self):
        response = self.client().get('/categories/2')
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['currentCategory'], 'Art')

        # Udacity requirements:
        # Question categoray Should equal 2 same as url
        self.assertEqual(res['questions'][0]['category'], 2)

        self.assertTrue(res['questions'])
        self.assertTrue(res['total_questions'])

    # ------------- TEST 2  ------ Bad request ---------------------
    # Random category that does not exisit
    def test_questions_by_category(self):
        response = self.client().get('/categories/20202021')
        self.assertEqual(response.status_code, 404)

    # ------------- TEST 3  ------ Correct request ---------------------

    def test_get_by_search(self):
        response = self.client().post(     # Udacity requirements:  word = title
            '/search/questions', json={'searchTerm': 'title'})
        res = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        # There's a question and an answer
        self.assertTrue(res['questions'][0]['question'])
        self.assertTrue(res['questions'][0]['answer'])

    # ------------- TEST 3  ------ Bad request ---------------------
    def test_get_by_search(self):
        # ------------------------------------- BAD JSON DATA ---- Front end should send 'searchTerm' as key ------
        response = self.client().post(
            '/search/questions', json={'RandomThing': 'title'})

        # 422 ( Unprocessable entity )  is expected
        self.assertEqual(response.status_code, 422)

    # ------------- TEST 4  ------ Correct request ---------------------
    def test_add_question(self):

        # Question data to be inserted
        question_json = {
            'question': 'Who wrote this',
            'answer': 'Sal7one',
            'difficulty': 1,
            'category': '2'
        }
        response = self.client().post('/questions/add', json=question_json)
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        # Question added successfuly
        self.assertEqual(res['success'], True)

    # ------------- TEST 4  ------ Bad request ---------------------
    def test_add_question(self):

        # Question data to be inserted
        question_json = {
            'question': 'Who wrote this',
            'answer': 'Sal7one',
            # Should cause a 422 ( Unprocessable entity )
            'difficulty': 'This should be an integer',
            'category': '2'
        }
        response = self.client().post('/questions/add', json=question_json)
        self.assertEqual(response.status_code, 422)

    # ------------- TEST 5  ------ Correct request ---------------------

    def test_get_all_categories(self):
        response = self.client().get('/categories/all')
        res = response.data

        self.assertEqual(response.status_code, 200)
        self.assertTrue(res['categories'])

    # ------------- TEST 5  ------ Bad request ---------------------
    def test_get_all_categories(self):
        # Post - > "method not allowed" expecting 405
        response = self.client().post('/categories/all')
        self.assertEqual(response.status_code, 405)

    # ------------- TEST 6  ------ Correct request ---------------------

    def test_delete_question(self):
        response = self.client().delete('/questions/3/delete')
        res = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['success'], True)

    # ------------- TEST 6  ------ Bad request ---------------------
    def test_delete_question(self):
        # Question 50000000 Not found  expecting 404
        response = self.client().delete('/questions/50000000/delete')
        self.assertEqual(response.status_code, 404)

    # ------------- TEST 7  ------ Correct request ---------------------
    def test_make_quiz(self):
     # quiz data to be worked with
        quiz_json = {
            'previous_questions': [],
            'quiz_category': {'id': 2},
        }
        response = self.client().post('/quizzes/questions', json=quiz_json)
        res = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        # We got a quesiton and an answer
        self.assertTrue(res['question'])
        self.assertTrue(res['question']['answer'])

    # ------------- TEST 7  ------ Bad request ---------------------

    def test_make_quiz(self):
     # quiz data to be worked with
        quiz_json = {
            'previous_questions': [],
            'quiz_category': {'id': 66},
        }
        response = self.client().post('/quizzes/questions', json=quiz_json)
        
        # We Don't have a quesiton in  category 66 (does not exisit)
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
