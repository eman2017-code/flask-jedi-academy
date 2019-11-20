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

# this shows all the courses that a padawan has
@courses.route('/', methods=['GET'])
@login_required
def courses_index():
    try:
        # we want to see the course instance that coorelates with the padawan
        this_users_course_instances = models.Course.select().where(models.Course.owner_id == current_user.id)
        # we need to loop through the courses to show them for the padawan
        this_padawans_course_dicts = [model_to_dict(course) for course in this_users_course_instances]

        return jsonify(data=this_padawans_course_dicts, status={
            'code': 200,
            'message': 'Success'
            }), 200

    # if the model does not exist
    except models.DoesNotExist:
        # return the error
        return jsonify(data={}, status={
            'code': 401, 
            'message': "Error getting the resources"
            }), 401

# @courses.route('/<padawans>', methods=['GET'])
# @login_required
# def get_courses():
#     #Some kind of logic involving whether user is admin...
#     #Find all Padawans in a course
#     #Again, foreign key for courses in padawans?
#     try:
#         this_course_padawan_instances = models.Course.select(models.Course.padawan_id)
#         this_padawans_course_dicts = [model_to_dict(course) for course in this_course_padawan_instances]

#         return jsonify(data=this_padawans_course_dicts, status={
#                 'code': 200,
#                 'message': 'Success'
#             }), 200

#     except models.DoesNotExist:
#         return jsonify(data={}, status={
#                 "code": 401, 
#                 "message": "Error getting the resources"
#             }), 401
    


