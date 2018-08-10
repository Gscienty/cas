from cas.extensions import db

class TicketGrandTicket(db.Model):
    __tablename__ = 'ticket_grant_ticket'
    
    token = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)
    expire = db.Column(db.TIMESTAMP, nullable=False)
