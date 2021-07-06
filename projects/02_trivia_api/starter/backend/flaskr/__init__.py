import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


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

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    # Helper function to create Questions objects
    def getQuestionList(all_questions):
        question_list = []

        for question in all_questions:
            current_question = {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "category": question.category,
                "difficulty": question.difficulty}
            question_list.append(current_question)
        return question_list
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
                question_list = getQuestionList(all_questions)

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

                question_list = getQuestionList(all_questions)

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
                question_list = getQuestionList(all_questions)

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

    @app.route('/questions/')
    def retrieve_questions():
        page = request.args.get('page', default=1, type=int)
        result = getQuestions(page)

        question_data = result
        if(len(question_data) == 0):
            abort(400)

        return jsonify(question_data)

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

    @app.route('/search/questions', methods=["POST"])
    def get_by_search():
        search_term = request.json.get('searchTerm')
        print(search_term)

        # Helper function to get searched questions
        result = getQuestions(1, 0, search_term)
        # question_data = result
        # if(len(question_data) == 0):
        #   abort(400)

        return result
    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
