import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel

import logging
logger = logging.getLogger('console')

class Auth():
    """
    Auth Class
    """

    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """

        logger.info(user_id)
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            logger.info(payload)
            encoded = jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            )
            logger.info(encoded)
            logger.info(type(encoded))

            #token = encoded.decode("utf-8")
            #logger.info(token)
            #logger.info(type(token))
            return encoded
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error in generating user token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            logger.info(token)
            logger.info(type(token))
            logger.info(os.getenv('JWT_SECRET_KEY'))
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])

            logger.info(payload)
            logger.info(type(payload))            
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    # decorator
    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)

            logger.info(data)
            logger.info(type(data))

            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth