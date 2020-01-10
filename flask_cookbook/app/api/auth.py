from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_restplus import Namespace, Resource

from flask_cookbook.app.core.auth_service import AuthService

api = Namespace('auth', description='Used to authenticate user.')


@api.route('/signin/<string:username>')
class UserSignIn(Resource):
    def post(self, username):
        current_user = AuthService.get_user_by_username(username)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(username)}, 401
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {
                   'user': {
                       "username": username,
                       "email": current_user.email,
                   },
                   'access_token': access_token,
                   'refresh_token': refresh_token
               }, 200
