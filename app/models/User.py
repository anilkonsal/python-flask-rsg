from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from .. import login_manager
from .. import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    password_reset_token = db.Column(db.String(128))

    def __init__(self, name, email, password):
        self.name = name,
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('Password is not a readable property')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'token': self.id})
        self.password_reset_token = token
        db.session.add(self)
        return token

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('token') != self.id:
            return False
        self.password_reset_token = None
        db.session.add(self)
        return True

    @staticmethod
    def load_user_by_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user_id = data.get('token')
        return User.query.get(int(user_id))
   
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

