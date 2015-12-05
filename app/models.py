__author__ = 'johnedenfield'

from sqlalchemy import desc, asc
from app import db
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify

import datetime, markdown, os




class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    posted = db.Column(db.Boolean)

    @classmethod
    def all(cls):
        return Article.query.order_by(desc(Article.created)).all()

    @classmethod
    def find_by_id(cls, id):
        return Article.query.filter(Article.id == id).first()

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @property
    def html(self):
        return markdown.markdown(self.body)



class Photo(db.Model):
    __tablename__='photos'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Article.id, onupdate="CASCADE", ondelete="CASCADE"))

    filename = db.Column(db.String(100))
    caption = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    display_order = db.Column(db.Integer)

    @classmethod
    def find_by_article_id(cls, id):
        return Photo.query.filter(Photo.post_id == id).order_by(asc(Photo.created)).all()

    @classmethod
    def find_by_id(cls, id):
        return Photo.query.filter(Photo.id == id).first()

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @property
    def file_url(self):
        return url_for('static',filename =os.path.join('photos', self.filename))



# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    pwdhash = db.Column(db.String)

    def __init__(self,username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def get_id(self):
        return unicode(self.id)