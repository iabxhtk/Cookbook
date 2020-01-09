from flask_restplus import Api
from .cookbook import api as cookbook_api
from .auth import api as auth_api

api = Api()
api.add_namespace(cookbook_api)
api.add_namespace(auth_api)
