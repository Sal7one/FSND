# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

> Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. _./backend/flaskr/`__init__.py`_
2. _./backend/test_flaskr.py_

### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. _./frontend/src/components/QuestionView.js_
2. _./frontend/src/components/FormView.js_
3. _./frontend/src/components/QuizView.js_

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [README within ./frontend for more details.](./frontend/README.md)

## API Reference

### Getting Started

- Backend Base URL: `http://127.0.0.1:5000/`
- Frontend Base URL: `http://127.0.0.1:3000/`
- Authentication: Authentication or API keys are not used in the project yet.

### Error Handling

Errors are returned in the following json format:

```json
{
  "error": 404,
  "message": "Resource Not Found",
  "success": false
}
```

The error codes currently returned are:

- 400 – Bad request
- 404 – Resource not found
- 405 - Method Not Allowed
- 422 – Unprocessable entity
- 500 – Internal server error

### Endpoints

#### GET /questions/

- General:

  - Returns all questions
  - questions are paginated you get 10.
  - pages could be requested by a query string

- Sample: `curl http://127.0.0.1:5000/questions/`<br>

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "currentCategory": "",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "12345",
      "category": 5,
      "difficulty": 5,
      "id": 25,
      "question": "as"
    }
  ],
  "success": true,
  "total_questions": 43
}
```

#### GET /categories/all

- General:

  - Returns all the categories.

- Sample: `curl http://127.0.0.1:5000//categories/all`

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

#### DELETE /questions/<int:id\>/delete

- General:

  - Deletes a question by id form the url parameter.

- Sample: `curl http://127.0.0.1:5000/questions/22/delete -X DELETE`

```json
{
  "message": "Question Deleted.",
  "success": true
}
```

#### POST /questions/add

- General:

  - Creates a new question based on a payload.

- Sample: `curl -XPOST -H "Content-type:application/json" -d "{ "question": "SomeQuestions?", "answer": "GoodAnswer", "difficulty": 1, "category": "2" }" "http://127.0.0.1:5000/questions/add`

```json
{
  "message": "Question created.",
  "success": true
}
```

#### POST /questions/search

- General:

  - returns any question that has a string matching the one sent

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type:application/json" -d '{"searchTerm": "play"}'`

```json
{
  "currentCategory": "",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### GET /categories/<int:id\>

- General:
  - Gets questions by category using the id provided
- Sample: `curl http://127.0.0.1:5000/categories/5`<br>

```json
{
  "currentCategory": "Entertainment",
  "questions": [
    {
      "answer": "12345",
      "category": 5,
      "difficulty": 5,
      "id": 25,
      "question": "as"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST /quizzes/questions

- General

  - Takes the category and previous questions in the request.
  - Return random question not in previous questions.

- Sample: `curl -XPOST -H "Content-type:application/json" -d "{"previous_questions": [], "quiz_category": {"type": "All", "id": 0} }" "http://127.0.0.1:5000/quizzes/questions`

```json
{
  "question": {
    "answer": "Sal7one",
    "category": 2,
    "difficulty": 1,
    "id": 72,
    "question": "Who wrote this"
  },
  "success": true
}
```

#### DevNote

- Sometimes charcater escapes are necessary to make curl send the object correctly \"quiz_category\" for example. I recommend using PostMan instead of windows cmd

#### Authors

- All starter project rights go to udacity

- Front-end enhancment by Github: @iMishaDev, and small updates by me Github: @Sal7one

- All backend and testing code has been wrriten by me Github: @Sal7one
