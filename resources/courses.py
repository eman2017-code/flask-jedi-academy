import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

courses = Blueprint('courses', 'courses')

# create route that allows only the admin to create a class
@courses.route('/', methods=["POST"])
# the user (admin) must be logged in to do this
@login_required
def create_course():
    payload = request.get_json()
    # this is creating the course
    # set up a flag
    # if the current user is an admin they can do this, otherwise they cannot
    if current_user.full_name == 'admin':
        # they will create the course
        course = models.Course.create(title=payload["title"], description=payload["description"])

        # we have to change the model to a dictionary
        course_dict = model_to_dict(course)

        return jsonify(data=course_dict, status={"code": 201, "message": "Success!"}), 201
        print('you are able to create a course because you are an admin')
    else:
        print('you are not able to create a course because you are not an admin')
    


# @courses.route('/', methods=["POST"])
# @login_required
# def create_course():
#     payload = request.get_json()

#     course = models.Course.create(name=payload['title'], 
#         owner=current_user.id, 
#         description=payload["description"]
#     )

#     # Change the model to a dict
#     print(model_to_dict(course), 'model to dict')
#     course_dict = model_to_dict(course)
#     # delete the password
#     # course_dict['owner'].pop('password')
#     return jsonify(data=dog_dict, status={"code": 201, "message": "Success"}), 201

