from cas.extensions import db
from flask_sqlalchemy import sqlalchemy
import uuid
import time
import datetime

class ServerTicket(db.Model):
    __tablename__ = 'server_ticket'
    
    token = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    domain = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)
    expire = db.Column(db.TIMESTAMP, nullable=False)
    
    def create(domain, username, expireDuration):
        originToken = username + str(time.time())
        token = str(uuid.uuid5(uuid.NAMESPACE_OID, originToken))
        expire = datetime.datetime.now() + datetime.timedelta(seconds=expireDuration)
        
        st = ServerTicket()
        
        st.token = token
        st.username = username
        st.domain = domain
        st.create_time = datetime.datetime.now()
        st.expire = expire
        
        db.session.add(st)
        db.session.commit()
        
        return st
    
    def __get(token):
        return ServerTicket.query.filter(sqlalchemy.and_(ServerTicket.token == token,
                                                         ServerTicket.expire >= datetime.datetime.now())).first()
    
    def exist(token):
        st = ServerTicket.__get(token)    
        return st is not None
    
    def get(token):
        st = ServerTicket.__get(token)
        if st is None:
            return None
        return st.username, st.domain
