from flask_cookbook.app.model.auth import UserModel


class AuthService:
    @staticmethod
    def get_user_by_username(username):
        return UserModel.query.filter_by(username=username).first()
