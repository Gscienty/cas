from flask_restful import Resource, reqparse, HTTPException
import re
from cas.models.application import Application
from cas.models.user import User

DOMAIN_REGEX = r'^https?:\/\/([^\/]+)'

class DomainNotExistError(HTTPException):
    code=401
    description='domain_not_exist'

class DomainFormatError(HTTPException):
    code=400
    description='domain_format_error'

class DomainNotAvailableError(HTTPException):
    code=403
    description='domain_not_available'

class UserNotExistError(HTTPException):
    code=404
    description='user_not_exist'

class UserLockedError(HTTPException):
    code=401
    description='user_locked'

class LoginResource(Resource):
    def __init__(self):
        self.getParamParser = reqparse.RequestParser()
        self.getParamParser.add_argument('callback_url', type=str, location=[ 'args' ])

        self.postParamParser = reqparse.RequestParser()
        self.postParamParser.add_argument('username', type=str, location=[ 'json' ])
        self.postParamParser.add_argument('password', type=str, location=[ 'json' ])
        self.postParamParser.add_argument('callback_url', type=str, location=[ 'json' ])

    def __assertDomain(self, callbackURL):
        if callbackURL is None:
            raise DomainNotExistError()
        if not re.match(DOMAIN_REGEX, callbackURL):
            raise DomainFormatError()

        domain = re.search(DOMAIN_REGEX, callbackURL).group(1)
        if not Application.existDomain(domain):
            raise DomainNotExistError()
        
        appInfo = Application.get(domain)
        if appInfo.available == False:
            raise DomainNotAvailableError()

        return appInfo


    def get(self):
        param = self.getParamParser.parse_args()
        callbackURL = param.callback_url

        appInfo = self.__assertDomain(callbackURL)
        
        return { 'name': appInfo.name }, 200

    def post(self):
        param = self.postParamParser.parse_args()

        self.__assertDomain(param.callback_url)

        if not User.exist(param.username, param.password):
            raise UserNotExistError()

        user = User.get(param.username)
        if user.available is False:
            raise UserLockedError()

        return { 'message': 'login_success' }, 302, { 'Location': param.callback_url }
