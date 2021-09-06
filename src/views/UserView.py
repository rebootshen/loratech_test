from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth


import json
from marshmallow import ValidationError


user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()
#logger = logging.getLogger('flask.app')
import logging
logger = logging.getLogger('console')


@user_api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()

    logger.info(req_data)
    logger.info(type(req_data))
    str1 = json.dumps(req_data)
    logger.info(str1)
    logger.info(type(str1))

    if not req_data:
        return custom_response("No input data provided", 400)
    # Validate and deserialize input
    try:
        data = user_schema.load(req_data)
    except ValidationError as err:
        return custom_response(err.message, 422)

    logger.info(data)
    logger.info(type(data))

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()
    ser_data = user_schema.dump(user)

    logger.info(ser_data)
    logger.info(type(ser_data))
    ido = ser_data.get('id')
    logger.info(ido)
    logger.info(type(ido))
    token = Auth.generate_token(ido)
    logger.info("token:begin")
    logger.info(token)
    logger.info(type(token))
    logger.info("token:end")
    message = {'jwt_token': token}
    return custom_response(message, 201)

@user_api.route('/login', methods=['POST'])
def login():
    """
    User Login Function
    """
    req_data = request.get_json()

    if not req_data:
        return custom_response("No input data provided", 400)
    # Validate and deserialize input
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err.message, 422)
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))
    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))
    return custom_response({'jwt_token': token}, 200)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    logger.info(user)
    logger.info(type(user))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)

@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
    Get all users
    """
    users = UserModel.get_all_users()
    logger.info(users)
    logger.info(type(users))

    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    logger.info(req_data)
    logger.info(type(req_data))

    if not req_data:
        return custom_response("No input data provided", 400)
    # Validate and deserialize input
    try:
        data = user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(err.message, 422)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserModel.get_one_user(g.user.get('id'))
    logger.info(user)
    logger.info(type(user))
    user.delete()

    #ser_user = user_schema.dump(user)
    message = {'message': str(user.id) + ' deleted'}
    logger.info(message)
    return custom_response(message, 204)




def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )