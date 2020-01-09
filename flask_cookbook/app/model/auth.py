from flask_cookbook.app import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(120), nullable=False)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_jwt_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
