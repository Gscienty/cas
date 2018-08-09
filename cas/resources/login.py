from flask_restful import Resource, reqparse, HTTPException
import re
from cas.models.application import Application

DOMAIN_REGEX = r'^https?:\/\/([^\/]+)'

class DomainNotExistError(HTTPException):
    code=401
    description='domain_not_exist'

class DomainFormatError(HTTPException):
    code=400
    description='domain_format_error'

class DomainNotAvailableError(HTTPExpection):
    code=403
    description='domain_not_available'

class LoginResource(Resource):
    def __init__(self):
        self.getRequestParam = reqparse.RequestParser()
        self.getRequestParam.add_argument('callback_url', type=str, location=[ 'args' ])

    def get(self):
        param = self.getRequestParam.parse_args()
        callbackURL = param.callback_url

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
        
        return { 'name': appInfo.name }, 200
