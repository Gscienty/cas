from flask_restful import Resource, reqparse, HTTPException
from flask import request
import re
from cas.models.application import Application
from cas.models.user import User
from cas.models.ticket_grant_ticket import TicketGrantTicket
from cas.models.server_ticket import ServerTicket

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
        self.getParamParser.add_argument('domain', type=str, location=[ 'args' ])

        self.postParamParser = reqparse.RequestParser()
        self.postParamParser.add_argument('username', type=str, location=[ 'json' ])
        self.postParamParser.add_argument('password', type=str, location=[ 'json' ])
        self.postParamParser.add_argument('domain', type=str, location=[ 'json' ])

        
    def __assertDomain(self, domain):
        if domain is None:
            raise DomainNotExistError()
        if not Application.existDomain(domain):
            raise DomainNotExistError()
        
        appInfo = Application.get(domain)
        if appInfo.available == False:
            raise DomainNotAvailableError()

        return appInfo
    
    def get(self):
        param = self.getParamParser.parse_args()
        appinfo = self.__assertDomain(param.domain)
        
        if 'ticket_grant_ticket' in request.cookies:
            tgtToken = request.cookies['ticket_grant_ticket']
            tgt = TicketGrantTicket.get(tgtToken)
            
            st = ServerTicket.create(param.domain, tgt.username, appinfo.st_expire)
            
            return {
                'message': 'login_success',
                'server_ticket': st.token
            }, 302, { 'Location': '%s?token=%s' % (appInfo.callback_url, st.token) }
        
        return { 'name': appinfo.name }, 200
    
    def post(self):
        param = self.postParamParser.parse_args()

        appinfo = self.__assertDomain(param.domain)

        if not User.exist(param.username, param.password):
            raise UserNotExistError()

        user = User.get(param.username)
        if user.available is False:
            raise UserLockedError()
        
        tgt = TicketGrantTicket.create(param.username, appinfo.tgt_expire)
        st = ServerTicket.create(param.domain, param.username, appinfo.st_expire)
        
        return {
            'message': 'login_success',
            'ticket_grant_ticket': tgt.token,
            'server_ticket': st.token
        }, 302, {
            'Location': '%s?token=%s' % (appInfo.callback_url, st.token),
            'Set-Cookie': 'ticket_grant_ticket=%s; Expire=%d; Path=/; HttpOnly' % (tgt.token, appinfo.tgt_expire)
        }
