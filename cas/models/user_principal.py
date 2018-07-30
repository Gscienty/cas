from cas.extensions import db
from flask_sqlalchemy import sqlalchemy

class UserPrincipal(db.Model):
    __tablename__ = 'user_principal'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    profile = db.Column(db.Text, nullable=True)

    def exist(username, password):
        result = UserPrincipal.query.filter(sqlalchemy.and_(UserPrincipal.username == username, UserPrincipal.password == password)).first()
        return result is not None

    def get(username):
        return UserPrincipal.query.filter(UserPrincipal.username == username).first()
