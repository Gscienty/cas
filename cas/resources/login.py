from flask_restful import Resource, reqparse, HTTPException
import re

class DomainNotExistError(HTTPException):
    code=401
    description='domain_not_exist'

class LoginResource(Resource):
    def __init__(self):
        self.getRequestParam = reqparse.RequestParser()
        self.getRequestParam.add_argument('callback_url', type=str, location=[ 'args' ])

    def get(self):
        param = self.getRequestParam.parse_args()
        callbackURL = param.callback_url

        if callbackURL is None:
            raise DomainNotExistError()
        return callbackURL
        # domain_regex = r'^https?:\/\/([^\/\\].*)(\/.*)?$'

        # return re.search(domain_regex, callbackURL).group(0)
