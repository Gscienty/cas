from flask_restful import Resource, reqparse, HTTPException
from cas.models.server_ticket import ServerTicket
from cas.models.user_permission import UserPermission


class ServerTicketNotExistError(HTTPException):
    code=404
    description='server_ticket_not_exist'


class ServerValidate(Resource):
    

    def __init__(self):
        self.getParamParser = reqparse.RequestParser()
        self.getParamParser.add_argument('token', type=str, location=[ 'args' ])

    def get(self):
        param = self.getParamParser.parse_args()
        if not ServerTicket.exist(param.token):
            raise ServerTicketNotExistError()
        username, domain = ServerTicket.get(param.token)
        
        tags = UserPermission.tags(username, domain)
        result = []
        for tag in tags:
            result.append(tag)
        return result, 200
