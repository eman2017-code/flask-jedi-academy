from flask import Flask, jsonify, g
from flask_cors import CORS

from flask_login import LoginManager

from resources.courses import courses
from resources.padawans import padawans
from resources.enrollments import enrollments

import models

DEBUG = True 
PORT = 8000

app = Flask(__name__)  

app.secret_key = "this is a secret key that only the jedi can see"

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_padawan(padawan_id):
  try: 
    return models.Padawan.get(models.Padawan.id == padawan_id)
  except models.DoesNotExist:
    return None

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(data={'error': 'User not logged in.'}, status={'code': 401,'message': "You must be logged in to access that resource."}), 401

CORS(courses, origins=['http://localhost:3000'], supports_credentials=True) 
CORS(padawans, origins=['http://localhost:3000'], supports_credentials=True)
CORS(enrollments, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(courses, url_prefix='/api/v1/courses')
app.register_blueprint(padawans, url_prefix='/api/v1/padawans')
app.register_blueprint(enrollments, url_prefix='/api/v1/enrollments')

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