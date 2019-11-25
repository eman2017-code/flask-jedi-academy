import models

from flask import request, jsonify, Blueprint

from peewee import DoesNotExist

from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import login_user, current_user, logout_user, login_required

from playhouse.shortcuts import model_to_dict

# make this a blueprint
padawans = Blueprint('padawans', 'padawans')

# register route
@padawans.route('/register', methods=["POST"])
def register():
    # grab the padawan
    payload = request.get_json()
    # make it email lowercase
    payload['email'].lower()

    try:
        # query/check their full_name against the database
        models.Padawan.get(models.Padawan.full_name == payload['full_name'])

        # return the error if there is an email like that that already exists in the database
        return jsonify(
            data={},
            status={"code": 401,
                    "message": 'A user will that full_name already exists'}
        ), 401

    except DoesNotExist:

        try:
            # query/check their email against the database
            models.Padawan.get(models.Padawan.email == payload['email'])

            # return the error if there is an email like that that already exists in the database
            return jsonify(
                data={},
                status={"code": 401,
                        "message": "A user will that email already exists"}
            )

            # if the user does not already exist in the database via full_name
        except DoesNotExist:

            # if the user was not already in the database
            payload['password'] = generate_password_hash(payload['password'])

            # spread operator
            padawan = models.Padawan.create(**payload)

            # this logs them in
            login_user(padawan)

            # make into dictionary
            padawan_dict = model_to_dict(padawan)

            # delete password
            del padawan_dict['password']

            # return good response
            return jsonify(
                data=padawan_dict,
                status={"code": 201, "message": "Successfully registered {}".format(
                    padawan_dict['full_name'])}
            ), 201


# login route
@padawans.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    try:
        # look up padawan by full_name
        padawan = models.Padawan.get(
            models.Padawan.full_name == payload['full_name'])
        # convert padawan into dictionary
        padawan_dict = model_to_dict(padawan)
        # check padawan's password using bcrypt
        if(check_password_hash(padawan_dict['password'], payload['password'])):
            # how we actually log in the user
            login_user(padawan)
            del padawan_dict['password']
            # return good news
            return jsonify(data=padawan_dict, status={'code': 200, 'message': "Succesfully logged in {}".format(padawan_dict['full_name'])}), 200
        else:
            # return the error
            return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401
    except models.DoesNotExist:
        # the email is not found
        return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401

# logout route
@padawans.route('/logout', methods=['GET'])
def logout():
    # get the full name of the user
    full_name = model_to_dict(current_user)['full_name']
    # actually logs the user out
    logout_user()
    # nice message for the user
    return jsonify(data={}, status={
        'code': 200,
        'message': "Successfully logged out {}".format(full_name)
    })

# route for admin to see all students
@padawans.route('/', methods=["GET"])
def list_all_padawans():
    if current_user.full_name == 'admin':
        # declare payload variable
        payload = request.get_json()
        # select all the padawans
        padawan_instances = models.Padawan.select()
        # loop through all the padawan ids (convert to dictionaries)
        padawan_instances_dict = [model_to_dict(
            padawans) for padawans in padawan_instances]
        # return the list of padawans dicts
        return jsonify(data=padawan_instances_dict, status={
            'code': 200,
            'message': "you will be able to see all the students in the school"
        })
    else:
        return jsonify(data={}, status={
            'code': 401,
            'message': "You will NOT be able to see all the students in the school"
        })


# this shows all the courses that a padawan is enrolled in
@padawans.route('/<padawan_id>', methods=['GET'])
# @login_required
def courses_index(padawan_id):
    # try:

        # enr = models.Enrollments.select().where(models.Enrollments.padawan_id == current_user.id)
        # print("here is enr")
        # print(enr)
        # enr_dicts = [model_to_dict(e) for e in enr]
        # print("here is enr_dicts")
        # print(enr_dicts)
        # we want to see the course instance that coorelates with the padawan
    this_users_course_instances = models.Enrollments.select().where(models.Enrollments.padawan_id == current_user.id)
    # we need to loop through the courses to show them for the padawan
    this_padawans_course_dicts = [model_to_dict(enrollment) for enrollment in this_users_course_instances]
    return jsonify(data=this_padawans_course_dicts, status={
    # return jsonify(data="hey", status={
        'code': 200,
        'message': 'Success'
    }), 200
    # if the model does not exist
    # except models.DoesNotExist:
    #     # return the error
    #     return jsonify(data={}, status={
    #         'code': 401,
    #         'message': "Error getting the resources"
    #     }), 401



