import os
import re
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import false, null
from werkzeug.exceptions import NotFound

from werkzeug.utils import redirect


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the apps
    app = Flask(__name__)
    setup_db(app)
    '''
    DONE --   @TODO --  DONE 
        Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {'origins': '*'}})

    '''
    DONE --   @TODO --  DONE 
        Use the after_request decorator to set Access-Control-Allow
    '''
    # CORS Rules
    @app.after_request
    def after_request(response):

        # Allow only used methods
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    # Helper function to make the database requests
    def getQuestions(page, by_category_id=None, by_search=None):

        # We get the data diffrently based on the parameters  from the calling function

        # Setup for all cases, and avoiding repation
        response = {}

        try:

            # Case search term was suppiled
            if(by_search):
                all_questions = Question.query.filter(Question.question.ilike(f'%{by_search}%')).paginate(
                    page, QUESTIONS_PER_PAGE, False)

                all_questions_length = len(Question.query.filter(
                    Question.question.ilike(f'%{by_search}%')).all())

                all_questions = all_questions.items
                question_list = [question.format()
                                 for question in all_questions]

                response = {
                    'questions': question_list,
                    'total_questions': all_questions_length,
                    'currentCategory': ''
                }

            # Case category id was supplied
            elif(by_category_id):
                all_questions_length = len(Question.query.filter_by(
                    category=by_category_id).all())

                all_questions = Question.query.filter_by(
                    category=by_category_id).paginate(
                    page, QUESTIONS_PER_PAGE, False)
                all_questions = all_questions.items

                question_list = [question.format()
                                 for question in all_questions]

                currentCategory = Category.query.filter_by(
                    id=by_category_id).first()

                if(currentCategory != None):
                    currentCategory = currentCategory.type
                    response = {
                        'questions': question_list,
                        'total_questions': all_questions_length,
                        'currentCategory': currentCategory
                    }
                else:
                    response = None

            # Case none of the above were supplied get all data.
            else:
                all_questions_length = Question.query.all()
                all_questions = Question.query.paginate(
                    page, QUESTIONS_PER_PAGE, False)
                all_questions = all_questions.items
                question_list = [question.format()
                                 for question in all_questions]

                all_categories = Category.query.all()
                formatted_categories = [category.format()
                                        for category in all_categories]

                if(all_categories != None):
                    response = {
                        'questions': question_list,
                        'total_questions': len(all_questions_length),
                        'categories': formatted_categories,
                        'currentCategory': ''
                    }
                else:
                    response = None

            return response
        except:
            print(sys.exc_info())
            abort(500)

    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions/', methods=["GET"])
    def retrieve_questions():
        # Getting user data
        page = request.args.get('page', default=1, type=int)

        # Get Questions with helper function
        question_data = getQuestions(page)

        if question_data is NotFound or question_data is None:
            abort(404)

        return jsonify(question_data)

    '''
    DONE --   @TODO --  DONE 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<category_id>', methods=["GET"])
    def questions_by_category(category_id):

        page = request.args.get('page', default=1, type=int)
        # Due to front-end not handling pages correctly we always assume it's 1
        page = 1

        question_data = getQuestions(page, category_id)

        if question_data is NotFound or question_data is None:
            abort(404)

        return jsonify(question_data)

    '''
    DONE --   @TODO --  DONE 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions/search', methods=["POST"])
    def get_by_search():
        front_end_expected_json = "searchTerm"
        search_term = request.json.get(front_end_expected_json)

        # User messed with correct expected front end json
        if search_term is None:
            abort(422)

        # Helper function to get searched questions
        result = getQuestions(1, 0, search_term)
        question_data = result

        if question_data is NotFound or question_data is None:
            abort(404)

        return jsonify(question_data)

    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions/add', methods=["POST"])
    def add_question():

        # Getting user data and making sure it's the same data-type as DB MODEL

        question_data = request.json
        try:
            user_question = str(question_data['question'])
            user_answer = str(question_data['answer'])
            user_difficulty = int(question_data['difficulty'])
            user_category = str(question_data['category'])
        except:
            abort(422)
        # Checking if there's an input error and handling it as entry error
        if(user_question != "" and user_answer != "" and user_difficulty != None and user_category != ""):

            # Instace of DB object with our Data
            the_Question = Question(question=user_question, answer=user_answer,
                                    category=user_category, difficulty=user_difficulty)
            # Try inserting into DB
            try:
                the_Question.insert()
                return jsonify({"success": True})
            # Server error from SQL Alchemy
            except:
                print(sys.exc_info())
                abort(500)
        else:
            abort(422)

    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories/all', methods=["GET"])
    def get_all_categories():

        try:
            all_categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in all_categories]

        except:
            abort(500)
        if(all_categories is None):
            abort(404)

        return jsonify({"categories": formatted_categories})

    # Helper function to get a random question from DB
    def getRandomQuestion(quiz_category, previous_questions):

        # if quiz_category is  = 0, that means all questions without filter...
        #   ....This value of 0 is how the front-end wanted to be handled
        try:
            questions = None

            if quiz_category == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category).all()

                # No questions found
                if questions == []:
                    return None

            # Setup data needed to get a random question
            formatted_questions = [question.format() for question in questions]
            potential_questions = []
            choosen_question = ''

            # Check if the question is not in already displayed add it
            for questions in formatted_questions:
                if questions['id'] not in previous_questions:
                    potential_questions.append(questions)

            if len(potential_questions) > 0:
                choosen_question = random.choice(potential_questions)

            return choosen_question
        except:
            # Handle database error
            print(sys.exc_info())
            abort(500)

    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<question_id>/delete', methods=["DELETE"])
    def delete_question(question_id):

        the_question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if the_question != None:
            the_question.delete()
        else:
            abort(404)

        return jsonify({"success": True})

    '''
    DONE --   @TODO --  DONE 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that !=one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes/questions', methods=["POST"])
    def make_quiz():

        # Getting user data
        quiz_data = request.json
        previous_questions = quiz_data['previous_questions']
        quiz_category = quiz_data['quiz_category']['id']

        # Getting a random question using a helper function
        choosen_question = getRandomQuestion(quiz_category, previous_questions)

        return jsonify({
            "question": choosen_question
        })

    '''
    DONE --   @TODO --  DONE 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        print(sys.exc_info())
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        print(error)
        print(sys.exc_info())
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        print(error)
        print(sys.exc_info())
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        print(error)
        print(sys.exc_info())
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        print(sys.exc_info())
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
    return app
