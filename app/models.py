from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from app import login
from app import app
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(90), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)