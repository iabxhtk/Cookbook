from flask import request
from flask_restplus import Namespace, Resource, fields

from flask_cookbook.app.core.auth_service import AuthService

api = Namespace('auth', description='Used to authenticate user.')
create_user_api_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True, description="Name for the user"),
    'email': fields.String(required=True, description="Email for the user"),
    'password': fields.String(required=True, description="Password for the user")
})

signin_user_api_model = api.model('SignIn', {
    'username': fields.String(required=True, description="Name for the user"),
    'password': fields.String(required=True, description="Password for the user")
})


@api.route('/user')
class UserList(Resource):
    def get(self):
        """Returns all registered users"""
        return AuthService.get_all_users()


@api.route('/signin')
class UserSignIn(Resource):
    @api.response(404, 'User doesnt exist.')
    @api.response(200, 'User successfully logged in.')
    @api.response(403, 'Wrong credentials.')
    @api.expect(signin_user_api_model, validate=True)
    def post(self):
        """Signs in user and retrieves jwt tokens."""
        return AuthService.signin_user(request.json)


@api.route('/signup')
class UserSignUp(Resource):
    @api.response(409, 'User with given name or email already exists.')
    @api.response(201, 'User successfully created.')
    @api.expect(create_user_api_model, validate=True)
    def post(self):
        """Creates new user"""
        return AuthService.create_new_user(request.json)


@api.route('/token_check')
class TokenCheck(Resource):
    def get(self):
        """Check if jwt token is still valid."""
        return AuthService.check_token_validity()
