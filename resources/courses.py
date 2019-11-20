import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

courses = Blueprint('courses', 'courses')