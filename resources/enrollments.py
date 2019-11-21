import models

from flask import Blueprint, jsonify, request

from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

# blueprint
enrollments = Blueprint('enrollments', 'enrollments')

# allow user(padawan) to enroll in a course -- creating an enrollment
@enrollments.route('/<id>', methods=["POST"])
# the user must login to register for a course
@login_required
# the id that is being passed in is the course id
def enroll_padawan(id):
	# payload = request.get_json()
	try: 
		# create the enrollment and tie the course to the padawan
		new_enrollment = models.Enrollments.create(course_id = id, padawan_id = current_user.id)
		# return the good news

		new_enrollment_to_dict = model_to_dict(new_enrollment)


		return jsonify(data=new_enrollment_to_dict, status={"code": 201, "message": "Succesfully added course to your roster"}), 201
		
	# if the model does not exist
	except models.DoesNotExist:
		# return the bad news
		return jsonify(data={}, status={"code": 401, "message": "this padawan cannot register, the dark side resides in them'"}), 401
		# print('this padawan cannot register, the dark side resides in them')



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