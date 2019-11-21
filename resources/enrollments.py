import models

from flask import request, jsonify, Blueprint

from flask_login import login_user, current_user, logout_user

from playhouse.shortcuts import model_to_dict

# blueprint
enrollments = Blueprint('enrollments', 'enrollments')

# allow user to enroll in a course -- creating an enrollment
@enrollments.route('/<course_id>', methods=['POST'])
def enroll_padawan_to_course(course_id):
    
    new_enrollment = models.Enrollment.create({course_id: course_id, padawan_id: current_user.id})

    return jsonify(data=course_dict, status={
            'code': 201,
            "message": "Succesfully added course to your roster"
        }), 201


# @enrollments.route('/<course_id>', methods=['PUT'])
# @login_required
# def update_course(id):
# 	payload = request.get_json()

#     course = models.Courses.get_by_id(id)

#     if(course.owner.id == current_user.id):

#         course.title = payload['title'] if 'title' in payload else None  # update it if that key
#         course.start_date = payload['start_date'] if 'start_date' in payload else None 
      
#         course.save()

#         course_dict = model_to_dict(course)