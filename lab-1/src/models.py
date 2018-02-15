from itsdangerous import TimedSerializer, SignatureExpired, BadSignature
from db import db
from config import SECRET_KEY
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    signup_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    # Copied from
    # https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    @staticmethod
    def verify_auth_token(token):
        s = TimedSerializer(SECRET_KEY)
        try:
            data = s.loads(token, max_age=600)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data.get('user_id'))
        return user

