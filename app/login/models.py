__author__ = 'johnedenfield'


from app import  db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    pwdhash = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def get_id(self):
        return unicode(self.id)
