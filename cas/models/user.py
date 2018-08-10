from cas.extensions import db
from flask_sqlalchemy import sqlalchemy

class User(db.Model):
    __tablename__ = 'application_user'

    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    profile = db.Column(db.Text, nullable=True)

    def exist(username, password):
        result = User.query.filter(sqlalchemy.and_(User.username == username, User.password == password)).first()
        return result is not None

    def get(username):
        return User.query.filter(User.username == username).first()
