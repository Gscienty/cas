from flask import Flask
from flask_restful import Api
from cas.resources.login import LoginResource
from cas.resources.server_validate import ServerValidate
from cas.extensions import db

APP_NAME = 'cas'
app = Flask(APP_NAME)
app.config.from_pyfile('config.cfg')

api_register = Api(app)

api_register.add_resource(LoginResource, '/login')
api_register.add_resource(ServerValidate, '/server_validate')

db.init_app(app)
