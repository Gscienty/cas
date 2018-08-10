from cas.extensions import db

class UserPermission(db.Model):
    __tablename__ = 'user_permission'
    
    username = db.Column(db.String(64), primary_key=True)
    domain = db.Column(db.String(64), nullable=False)
    tag = db.Column(db.String(32), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
