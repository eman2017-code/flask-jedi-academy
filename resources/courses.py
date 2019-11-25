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
    # if the current user is an admin they can do this, otherwise they cannot
    if current_user.full_name == 'admin':
        # they will create the course
        course = models.Course.create(title=payload["title"], description=payload["description"], owner=current_user.id)
        # we have to change the model to a dictionary
        course_dict = model_to_dict(course)
        # return good response
        return jsonify(data=course_dict, status={"code": 201, "message": "Success!"}), 201
    else:
        # the user will not be able to do! Forbidden!
        return jsonify(data={}, status={"code": 403, "message": "The force is not so strong with you"}), 403

# admin can update a course
@courses.route('/<id>', methods=["PUT"])
# the user must be logged in
@login_required
def update_course(id): 
    payload = request.get_json()
    # if the user is admin
    if current_user.full_name == 'admin': 
        query = models.Course.update(**payload).where(models.Course.id==id) 
        query.execute() 
        return jsonify(data=model_to_dict(models.Course.get_by_id(id)), status={"code": 200, "message": "you update a course successfully"})
    else:  
        # they cannot because they are not the admin
        return jsonify(data={}, status={"code": 403, "message": "The force is not so strong with you"}), 403

# delete course route (must be an admin)
@courses.route('/<id>', methods=["Delete"])
@login_required
def delete_course(id):
    # if user is NOT admin, they cant do that
    if current_user.full_name != 'admin':
        return jsonify(data={}, status={"code": 401, "message": "you are not a jedi master! You cant do this because you are not an admin"}), 401
    else:

        # delete all enrollments with this course ID
        query = models.Enrollments.delete().where(models.Enrollments.course_id == id)
        num_deleted = query.execute()
        print("deleted this many enrollments:")
        print(num_deleted)

        # declare variable to obtain the id of the course
        course_to_delete = models.Course.get_by_id(id)
        # delete that instance of that course

        course_to_delete.delete_instance()
        return jsonify(data="Course was successfully deleted", status={"code": 200, "message": "Successfully delted course"}), 200


# this shows all padawans in a course
@courses.route('/<course_id>', methods=["GET"])
# the user must be logged in
@login_required
def courses_padawans(course_id):
    try:
        # get all the padawans
        # join the enrollments table (the through table) and select where all the course_id in the through table match the course that is put into the route
        padawans_instances = (models.Padawan.select().join(models.Enrollments).where(models.Enrollments.course_id == course_id))
        # we want to loop through all of the padawan_ids that are in that course and make them into dictionaries
        padawans_instances_dicts = [model_to_dict(padawans) for padawans in padawans_instances]
        # give them a good message
        return jsonify(data=padawans_instances_dicts, status={"code": 200, "messasge": "these are your fellow classmaates that are in this course"}), 200
    except models.DoesNotExist:
        # return the error
        return jsonify(data={}, status={"code": 401, "messsage": "Error getting this resource"}), 401

# list all the courses (padawan and admin can)
@courses.route('/', methods=["GET"])
@login_required
def list_courses():
    try:
        payload = request.get_json()
        # models.Course.select() is taking all of the data from the Course model and storing it into the course_instances varaible 
        course_instances = models.Course.select()
        # loop through the Course Model Data(course_instances) and converting to dictionaries for Python to read
        course_instances_dict = [model_to_dict(courses) for courses in course_instances]
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
