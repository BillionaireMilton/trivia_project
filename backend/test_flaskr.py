import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from accessibility import DB_TEST_NAME, DB_TEST_USER, DB_TEST_PASSWORD

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    NEW_QUESTION = {
        "question": "What's the formula of water",
        "answer": "H2O",
        "category": 1,
        "difficulty": 1
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_TEST_USER, DB_TEST_PASSWORD,'localhost:5432', self.database_name)
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

  
    # Test 1: GET all available categories
    
    def test_1_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # Test 2: GET all question including pagination (every 10 questions)
    def test_2_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test 3: GET 404 for retrieving questions beyond valid page
    def test_3_get_404_for_retrieve_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=10000', json={'category': 2})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    # Test 4: DELETE question based on question id
    def test_4_delete_question(self):
        response = self.client().delete('/questions/14')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 14)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    # Test 5: DELETE question that doesn't exists
    def test_5_delete_question_that_does_not_exists(self):
        response = self.client().delete('/questions/999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
    

    # Test 6: CREATE a new question
    def test_6_create_a_new_question(self):
        response = self.client().post('/questions', json=self.NEW_QUESTION)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    
    # Test 7: question creation not allowed 405 ERROR
    def test_7_405_question_creation_not_allowed(self):
        response = self.client().post('/questions/999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")
    
    # Test 8: get back question filtered by search term including pagination (every 10 question )
    def test_8_get_paginated_questions_search_with_result(self):
        response = self.client().post('/questions/search', json={'search': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 2)

    # Test 9: get  empty list of questions when search term doesn't retrieve any question
    def test_9_get_paginated_questions_search_without_result(self):
        response = self.client().post('/questions/search', json={'search': 'abracadabrabara'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['questions'])
        self.assertEqual(len(data['questions']), 0)
    
    # Test 10: get  panginated questions based on one category
    def test_10_get_paginated_questions_for_one_category(self):
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 4)
    
    # Test 11: get  404 error when categories doesn't exists
    def test_11_get_paginated_questions_for_not_existing_category(self):
        response = self.client().get('/categories/88/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test 12: get  quiz by category or all questions
    def test_12_post_quiz_by_category_or_all(self):
        questions_params = {
            'previous_questions': [17, 18],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }

        response = self.client().post('/quizzes', json=questions_params)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['previous_questions'])
        self.assertTrue(data['question'])

    # Test 13: get quizzes request without json data
    def test_13_post_quiz_without_parameters(self):
        
        response = self.client().post('/quizzes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

      
     



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()