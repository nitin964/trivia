## Trivia - The quiz game

Trivia is a virtual quiz game. This application can perform following functions:
1. Display questions - both all questions and by category. Each question shows the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions with answer, category and difficulty.
4. Search for questions based on a text query string which is case insensitive.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

# Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.


# Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

# Frontend
From the frontend folder, run the following commands to start the client:

npm install // only once to install dependencies
npm start 

By default, the frontend will run on localhost:3000.

# Tests
In order to run tests navigate to the backend folder and run the following commands:

dropdb trivia_test
createdb trivia_test
psql trivia_test < books.psql
python test_flaskr.py
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference
# Getting Started