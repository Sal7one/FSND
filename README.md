## Full Stack Web Developer Nanodegree (nd0044 v2)

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
