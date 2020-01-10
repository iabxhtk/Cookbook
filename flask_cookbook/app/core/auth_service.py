from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from marshmallow import fields, Schema
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cookbook.app import db
from flask_cookbook.app.model.auth import UserModel


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()


users_schema = UserSchema(many=True)


class AuthService:
    @staticmethod
    def get_user_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_username_or_email(username, email):
        return UserModel.query.filter((UserModel.email == email) | (UserModel.username == username)).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_pw_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def create_new_user(data):
        username = data['username']
        email = data['email']

        if AuthService.get_user_by_username_or_email(username, email):
            return {'message': 'Username {} or email {} already in use'.format(username, email)}, 409

        new_user = UserModel(
            username=username,
            email=email,
            password=AuthService.generate_hash(data['password'])
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return None, 201
        except Exception as e:
            print(e)
            return {'error': 'Something went wrong'}, 500

    @staticmethod
    def signin_user(data):
        username = data['username']
        password = data['password']
        current_user = AuthService.get_user_by_username(username)
        if not current_user:
            return {'error': 'User {} doesn\'t exist'.format(username)}, 404
        if AuthService.verify_pw_hash(password, current_user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)

            #revoked_token_store.set(access_jti, 'false', app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
           # revoked_token_store.set(refresh_jti, 'false', app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.2)
            return {
                       "username": current_user.username,
                       "email": current_user.email,
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'error': 'Wrong credentials'}, 403

    @staticmethod
    def get_all_users():
        return users_schema.dump(UserModel.query.all()), 200
