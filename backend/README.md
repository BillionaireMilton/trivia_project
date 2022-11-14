# Backend - Trivia API
## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

To get started navigate to the backend folder directly in your terminal and run `pip install requirements.txt`. All required packages are included in the requirements file. 

After installing all the dependencies in the requirements.txt file, run the following commands in order to start the flask App: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and which is a proxy in the frontend configuration. 

## Trivia API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None 
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET /questions?page=${integer}
- General:
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string
    - Request Arguments: None 
    - Returns: Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
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
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "totalQuestions": 22
}
```
#### GET /categories/${id}/questions
- General:
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: id - integer 
    - Returns: An object with questions for the specified category, total questions, and current category string
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 17,
    'currentCategory': 'History'
}
```
#### DELETE /questions/${id}
- General:
    - Deletes a specified question using the id of the question
    - Request Arguments: id - integer 
    - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/`
```
{
    'questions': True
    'deleted': question_id
}
```
#### POST /quizzes
- General:
    - Deletes a specified question using the id of the question
    - Request Body:
    ```
    {
        'previous_questions': [1, 4, 20, 15]
        'quiz_category': 'current category'
    }
    ```
    - Returns: a single new question object
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{'previous_questions': [1, 4, 20, 15], 'quiz_category': 'History'}" http://127.0.0.1:5000/quizzes`
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```
#### POST /questions
- General:
    - Sends a post request in order to add a new question
    - Request Body:
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
 ```
    Returns: Does not return any new data but the success state of the request
- Sample: `curl -X POST -H "Content-Type: application/json" -d “{ 'question':  'Here is a new question string', 'answer':  'Here is a new answer string', 'difficulty': 1, 'category': 3} http://127.0.0.1:5000/questions`
```
{
   "success": True',
   "created": question.id
 }
```
#### POST /questions
- General:
    - Sends a post request in order to search for a specific question by search term
    - Request Body:
```
{
    'searchTerm': 'this is the term the user is looking for'
}
 ```
    Returns: Does not return any new data but the success state of the request
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{"previous_questions": [1, 4, 20, 15], "quiz_category": "History"}" http://127.0.0.1:5000/quizzes`
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 17,
    'currentCategory': 'Entertainment'
}
```
