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
        self.database_name = "trivia"
        self.database_path = "postgresql://postgres:admin@{}/{}".format('localhost:5432', self.database_name)
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
    def test_get_paginated_questions(self):
        print ("test_get_paginated_questions")
        res = self.client().get("/questions")
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["currentCategory"], None)

    def test_get_categories(self):
        print ("test_get_categories")
        res = self.client().get("/categories")
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_delete_question(self):
        print ("test_delete_question")
        question = Question(question='test question', answer='test answer', difficulty=1, category=1)
        question.insert()
        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        ques = Question.query.filter(Question.id == question.id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(ques, None)

    def test_422_delete_nonexistend_question(self):
        print("test_404_delete_nonexistend_question")
        res = self.client().delete(f'/questions/2000')
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_create_question(self):
        print ("test_create_question")
        res = self.client().post(f'/add_questions', json={"question": "insert question", "answer": "insert answer", "difficulty": "1", "category": "1"})
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_create_question(self):
        print("test_422_create_question")
        res = self.client().post(f'/add_questions', json={"question": "insert question", "answer": "insert answer", "difficulty": "", "category": "1"})
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_question(self):
        print ("test_search_question")
        res = self.client().post(f'/search_questions', json={"searchTerm": "what"})
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], len(Question.query.filter(Question.question.ilike(f'%what%')).all()))

    def test_category_questions(self):
        print ("test_category_questions")
        res = self.client().get(f'/categories/1/questions')
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(Question.query.filter(Question.category == "1").all()))
    
    def test_404_category_questions(self):
        print("test_404_category_questions")
        res = self.client().get(f'/categories/10000/questions')
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_play_quiz(self):
        print ("test_play_quiz")
        jsonvalue = {'previous_questions': [], 'quiz_category': {'type': 'click', 'id': 1}}
        res = self.client().post(f'/quizzes', json=jsonvalue)
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_play_quiz(self):
        print ("test_play_quiz")
        jsonvalue = {'previous_questions': [], 'quiz_categories': {'type': 'click', 'id': 1}}
        res = self.client().post(f'/quizzes', json=jsonvalue)
        data = json.loads(res.data)
        print ("res.status_code" + str(res.status_code))
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
