from flask import Flask
from flask_restful import Api
from cas.resources.login import LoginResource
from cas.extensions import db

APP_NAME = 'cas'
app = Flask(APP_NAME)
app.config.from_pyfile('config.cfg')

api_register = Api(app)

api_register.add_resource(LoginResource, '/login')

db.init_app(app)
