import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
courses = Blueprint('courses', 'courses')

# admin create course route that allows (only the admin to create a class)
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
        course = models.Course.create(title=payload["title"], description=payload["description"], owner=current_user.id)

        # we have to change the model to a dictionary
        course_dict = model_to_dict(course)

        return jsonify(data=course_dict, status={"code": 201, "message": "Success!"}), 201
        print('you are able to create a course because you are an admin')
    else:
        # the user will not be able to do! Forbidden!
        return jsonify(data="Forbidden", status={"code": 403, "message": "The force is not so strong with you"}), 403
        print('you are not able to create a course because you are not an admin')

#admin can update(edit) a course (only an admin can do this)
@courses.route('/<id>', methods=["PUT"])
@login_required
def update_course(id): 

    payload = request.get_json()

    if current_user.full_name == 'admin': 

        query = models.Course.update(**payload).where(models.Course.id==id) 
        query.execute() 

        return jsonify(data=model_to_dict(models.Course.get_by_id(id)), status={"code": 200, "message": "you update a course successfully"})
    else:  

        return jsonify(data="Forbidden", status={"code": 403, "message": "The force is not so strong with you"}), 403
        print('you are not able to update a course because you are not an admin')


# this shows all the courses that a padawan has (padawan show page )
@courses.route('/<padawan_id>', methods=['GET'])
@login_required
def courses_index(padawan_id):
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

# list all the courses
@courses.route('/', methods=["GET"])
# @login_required
def list_courses():

    try:

        payload = request.get_json()
        print(payload)

        # models.Course.select() is taking all of the data from the Course model and
        # storing it into the course_instances varaible 
        course_instances = models.Course.select()

        #For loop through the Course Model Data(course_instances) and converting to dictionaries for Python to read
        course_instances_dict = [model_to_dict(courses) for courses in course_instances]

        print(course_instances)
        print("this my data >>>", course_instances_dict)

        # return the data 
        return jsonify(data=course_instances_dict, status={
                'code': 200,
                'message': 'Success'
                }), 200
    except:

        # return error message if data cannot be processed 
        return jsonify(data={}, status={
                'code': 500,
                'message': 'ops not good'
                }), 500










# # this shows all the padawans in a course 
# @courses.route('/<course_id>', methods=['GET'])
# # the user must be logged in
# @login_required
# def get_courses():
#     try:
#         # we need to get the course id
#         this_course_padawan_instances = models.Course.select(models.Course.owner_id)
#         console.log(owner_id)

#         # we need to loop through all the padawans_id that are associated with the course_id
#         # this_padawans_course_dicts = [model_to_dict(course) for course in this_course_padawan_instances]


#         return jsonify(data=this_padawans_course_dicts, status={
#                 "code": 200,
#                 "message": "Success"
#             }), 200

#     except models.DoesNotExist:
#         return jsonify(data={}, status={
#                 "code": 401, 
#                 "message": "Error getting the resources"
#             }), 401     

# # show all padawans in a course
# @courses.route('/<course_id>', methods=["POST"])
# # the user must be logged in
# def get_course():
#     try:
#         # find all the enrollments that have that course id
#         this_course_padawan_instances

#     # query for all the students that are paired with that course id in enrollments table

#     # return a list of all the students 




