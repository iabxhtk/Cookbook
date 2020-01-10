import os
from datetime import timedelta

base_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..'))


class Config:
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'change_this'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_project_dir, 'cookbook_test.db')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_project_dir, 'cookbook_dev.db')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)
    JWT_HEADER_TYPE = ''


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configurations = {'dev': DevelopmentConfig, 'test': TestingConfig, 'prod': ProductionConfig}
