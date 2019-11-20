import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

# make this a blueprint
enrollements = Blueprint('enrollements', 'enrollements')

# @enrollements.route('enroll/<current_user>/<course_id>', methods=['POST'])


@enrollements.route('/<padawan_id>', methods=['POST'])
def create_padawan_with_course(padawan_id):
    payload = request.get_json()
    course = models.Course.create(title=payload['title'], start_date=payload['start_date'], padawan=padawan_id)

    course_dict = model_to_dict(course)

    course_dict['padawan'].pop('password')

    return jsonify(data=course_dict, status={
            'code': 201,
            "message": "Succesfully created course with added padawan"
        }), 201


@enrollements.route('/<course_id>', methods=['PUT'])
@login_required
def update_course(id):
	payload = request.get_json()

    course = models.Courses.get_by_id(id)

    if(course.owner.id == current_user.id):

        course.title = payload['title'] if 'title' in payload else None  # update it if that key
        course.start_date = payload['start_date'] if 'start_date' in payload else None 
      
        course.save()

        course_dict = model_to_dict(course)