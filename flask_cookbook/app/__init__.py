from flask import Flask
from flask_bcrypt import Bcrypt

from flask_cookbook.app.api import api
from flask_cookbook.app.config import configurations
from flask_cookbook.app.model import db

b_crypt = Bcrypt()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(configurations[config_filename])

    db.init_app(app)
    b_crypt.init_app(app)
    api.init_app(app)
    return app
