from cas.extensions import db
from flask_sqlalchemy import sqlalchemy

class UserPermission(db.Model):
    __tablename__ = 'user_permission'
    
    permission_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    domain = db.Column(db.String(64), nullable=False)
    tag = db.Column(db.String(32), nullable=False)
    available = db.Column(db.Boolean, nullable=False)

    def tags(username, domain):
        permissions = UserPermission.query.filter(sqlalchemy.and_(UserPermission.username == username,
                                                                  UserPermission.domain == domain)).all()
        results = set()
        for permission in permissions:
            if permission.available is False:
                continue
            results.add(permission.tag)
        return results
