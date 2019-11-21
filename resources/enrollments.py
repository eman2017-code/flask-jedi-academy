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
	try: 
		# create the enrollment and tie the course to the padawan
		new_enrollment = models.Enrollments.create(course_id = id, padawan_id = current_user.id)
		# convert the enrollment into dictionary for Python to read
		new_enrollment_to_dict = model_to_dict(new_enrollment)
		# return good status
		return jsonify(data=new_enrollment_to_dict, status={"code": 201, "message": "Succesfully added course to your roster"}), 201
	# if the model does not exist
	except models.DoesNotExist:
		# return the error
		return jsonify(data={}, status={"code": 401, "message": "this padawan cannot register, the dark side resides in them'"}), 401