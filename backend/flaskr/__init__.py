from asyncio import exceptions
from logging import exception
import os
from sre_constants import CATEGORY_UNI_DIGIT
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app) 
    """
    @TODO: Completed 
    Set up CORS. Allow '*' for origins. Delete the sample route after 
    completing the TODOs
    """
    CORS(app)    
    """
    @TODO: Completed
     Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET,PUT,POST,DELETE,OPTIONS")
        return response
    """
    @TODO: Completed
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
    
        return jsonify(
            {
                'success': True,
                'categories': {category.id: category.type for category in
                               selection}
            }
        )
    """
    @TODO: Completed
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for
    three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(selection),
            'categories': {category.id: category.type for category in 
                           categories},
            'currentCategory': [cat.type for cat in categories]
        })
    """
    @TODO: Completed
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question
    will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = (Question.query.filter(Question.id == question_id).
                        one_or_none())
            question.delete()
            return jsonify({
                'success': True,
                'question_id': question_id
            })
        except:
            abort(422)
    """
    @TODO: Completed
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    """
    @app.route("/add_questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        if new_question in (None, ''):
            abort(422)
        if new_answer in (None, ''):
            abort(422)
        if new_difficulty in (None, ''):
            abort(422)
        if new_category in (None, ''):
            abort(422)

        cat = Category.query.filter(Category.id == new_category).one_or_none()

        if cat is None:
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, 
                                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
            })
        except:
            abort(422)
    """
    @TODO: Completed
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/search_questions", methods=["POST"])
    def srch_questions():
        body = request.get_json()
        searchterm = body.get('searchTerm', None)
        if searchterm:
            results = Question.query.filter(
                      Question.question.ilike(f'%{searchterm}%')).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in results],
                'totalQuestions': len(results),
                'currentCategory': None
            })
    """
    @TODO: Completed
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        try:
            questions = Question.query.filter(Question.category ==
                                            str(category_id)).all()
            
            if len(questions)==0:
                abort(404) 

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)
    """
    @TODO: Completed
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            prev_ques = body.get('previous_questions', None)
            cat = body.get('quiz_category', None)

            if cat['type'] == "click":
                questions = Question.query.filter(Question.id.notin_((
                                                  prev_ques))).all()
            else:
                questions = Question.query.filter_by(category=
                            str(cat['id'])).filter(Question.id.notin_(
                            (prev_ques))).all()

            question = (questions[random.randrange(0, len(questions))].format()
                        if len(questions) > 0 else None)
            
            return jsonify({
                'success': True,
                'question': question
            })
        except:
            abort(422)
    """
    @TODO: Completed
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
    
