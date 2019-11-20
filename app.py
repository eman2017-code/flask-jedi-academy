from flask import Flask, jsonify, g
from flask_cors import CORS

from flask_login import LoginManager

from resources.padawans import padawans
from resources.courses import courses

import models

DEBUG = True 
PORT = 8000

app = Flask(__name__)  

app.secret_key = "this is a secret key that only the jedi can see"

login_manager = LoginManager()

login_manager.init_app(app)

CORS(courses, origins=['http://localhost:3000'], supports_credentials=True) 
CORS(padawans, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(courses, url_prefix='/api/v1/padawans')
app.register_blueprint(padawans, url_prefix='/api/v1/courses')

@app.before_request 
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response 

# to test that this is actually working
@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__': 
  models.initialize()
  app.run(debug=DEBUG, port=PORT)