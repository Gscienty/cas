from cas.extensions import db
from flask_sqlalchemy import sqlalchemy
import uuid
import time
import datetime

class TicketGrantTicket(db.Model):
    __tablename__ = 'ticket_grant_ticket'
    
    token = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)
    expire = db.Column(db.TIMESTAMP, nullable=False)

    def create(username, expireDuration):
        originToken = username + str(time.time())
        token = uuid.uuid5(uuid.NAMESPACE_OID, originToken)
        expire = datetime.datetime.now() + datetime.timedelta(seconds=expireDuration)
        
        tgt = TicketGrantTicket()
        
        tgt.token = token
        tgt.username = username
        tgt.create_time = datetime.datetime.now()
        tgt.expire = expire
        
        db.session.add(tgt)
        db.session.commit()
        
        return tgt
    
    def __get(token):
        return TicketGrantTicket.query.filter(sqlalchemy.and_(TicketGrantTicket.token == token,
                                                              TicketGrantTicket.expire >= datetime.datetime.now())).first()
    def exist(token):
        tgt = TicketGrantTicket.__get(token)
        return tgt is not None
    
    def get(token):
        tgt = TicketGrantTicket.__get(token)
        if tgt is None:
            return None
        return tgt.username
