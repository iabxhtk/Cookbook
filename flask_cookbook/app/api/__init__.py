from flask_restplus import Api
from .cookbook import api as cookbook_api
from .auth import api as auth_api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(authorizations=authorizations)
api.add_namespace(cookbook_api)
api.add_namespace(auth_api)
