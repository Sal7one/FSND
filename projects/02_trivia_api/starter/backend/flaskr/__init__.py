import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from werkzeug.utils import redirect


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the apps
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {'origins': '*'}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    # CORS Rules
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Helper function to make the database requests

    def getQuestions(page, by_category_id=None, by_search=None):
        try:

            response = {}
            categories_list = {}
            all_categories = Category.query.all()

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
                print("searching")
            elif(by_category_id):

                all_questions_length = len(Question.query.filter_by(
                    category=by_category_id).all())
                print(all_questions_length)

                all_questions = Question.query.filter_by(
                    category=by_category_id).paginate(
                    page, QUESTIONS_PER_PAGE, False)
                all_questions = all_questions.items

                question_list = [question.format()
                                 for question in all_questions]

                currentCategory = Category.query.filter_by(
                    id=by_category_id).first().type

                response = {
                    'questions': question_list,
                    'total_questions': all_questions_length,
                    'currentCategory': currentCategory
                }

                print("by_id")
            else:
                all_questions_length = Question.query.all()
                all_questions = Question.query.paginate(
                    page, QUESTIONS_PER_PAGE, False)
                all_questions = all_questions.items
                question_list = [question.format()
                                 for question in all_questions]

                all_categories = Category.query.all()
                for category in all_categories:
                    categories_list[category.id] = category.type

                response = {
                    'questions': question_list,
                    'total_questions': len(all_questions_length),
                    'categories': categories_list,
                    'currentCategory': ''
                }

            return response
        except os.error as error:
            print("Server Error: Could not get Database data")
            print(error)
            return None
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
    @app.route('/questions/')
    def retrieve_questions():
        page = request.args.get('page', default=1, type=int)
        result = getQuestions(page)

        question_data = result
        if(len(question_data) == 0):
            abort(400)

        return jsonify(question_data)

    '''
    DONE --   @TODO --  DONE 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<category_id>')
    def questions_by_category(category_id):

        page = request.args.get('page', default=1, type=int)
        result = getQuestions(page, category_id)

        if(result == None):
            abort(500)
        question_data = result
        if(len(question_data) == 0):
            abort(400)

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

    @app.route('/search/questions', methods=["POST"])
    def get_by_search():
        search_term = request.json.get('searchTerm')
        print(search_term)

        # Helper function to get searched questions
        result = getQuestions(1, 0, search_term)
        # question_data = result
        # if(len(question_data) == 0):
        #   abort(400)

        return jsonify(result)

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

        question_data = request.json

        user_question = str(question_data['question'])
        user_answer = str(question_data['answer'])
        user_difficulty = int(question_data['difficulty'])
        user_category = str(question_data['category'])

        if(user_question != "" and user_answer != "" and user_difficulty != "" and user_category != ""):
            the_Question = Question(question=user_question, answer=user_answer,
                                    category=user_category, difficulty=user_difficulty)
            the_Question.insert()
            return jsonify({"success": True})
        else:
            abort(404)

        # # TODO EXCEPTION  HANDLING
        # # Helper function to get searched questions
        # # question_data = result
        # if(len(question_data) == 0):
        #     abort(400)

        # return jsonify({"success": True})
    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories/all', methods=["GET"])
    def get_all_categories():

        # Get all categories
        categories_list = {}
        all_categories = Category.query.all()
        for category in all_categories:
            categories_list[category.id] = category.type

        return jsonify({"categories": categories_list})

    # Helper function to get a random question from DB

    def getRandomQuestion(quiz_category, previous_questions):

        # Get all entries in Databse and choose a random ID

        # if quiz_category is  = 0, that means all questions without filter
        # This value of 0 is how the front-end wanted to be handled
        if quiz_category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category).all()

        formatted_questions = [question.format() for question in questions]
        potential_questions = []
        choosen_question = ''

        for questions in formatted_questions:
            if questions['id'] not in previous_questions:
                potential_questions.append(questions)

        if len(potential_questions) > 0:
            choosen_question = random.choice(potential_questions)

        return choosen_question

    '''
    DONE --   @TODO --  DONE 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<question_id>/delete', methods=["DELETE"])
    def delete_question(question_id):

        # TODO EXCEPTION  HANDLING
        the_question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if the_question != None:
            print(the_question)
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
    def quiz():

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
        return jsonify({
            "success": False,
            "error": error,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": error,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": error,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": error,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': error,
            'message': 'Internal server error'
        }), 500
    return app
