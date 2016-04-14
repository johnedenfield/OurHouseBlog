__author__ = 'johnedenfield'

from sqlalchemy import desc, asc
from app import app, db
from flask import url_for
from webhelpers.date import time_ago_in_words
from webhelpers.text import urlify
from werkzeug.utils import secure_filename
from PIL import Image

import datetime, markdown, os


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    posted = db.Column(db.Boolean)
    post_order = db.Column(db.Integer)

    @classmethod
    def all(cls):
        return Article.query.order_by(desc(Article.post_order)).all()

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
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Article.id, onupdate="CASCADE", ondelete="CASCADE"))

    filename = db.Column(db.String(100))
    caption = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    display_order = db.Column(db.Integer)
    rotate = db.Column(db.Integer)

    def upload(self, file_obj, id):
        self.filename = file_obj.filename
        self.post_id = id
        self.rotate = 0
        self.display_order = 0

        self.filename = str(id) + "_" + secure_filename(file_obj.filename)
        file_path = os.path.join(app.config['PHOTO_FOLDER'], self.filename)
        file_obj.save(file_path)

        self.websize()

        db.session.add(self)
        db.session.commit()

    def delete(self):
        filename = os.path.join(app.config['PHOTO_FOLDER'], self.filename)
        os.remove(filename)
        db.session.delete(self)
        db.session.commit()

    def rotate_photo(self, val):

        def rotate(fp,val):

            im = Image.open(fp)
            im_rot = im.rotate(val)
            im_rot.save(fp)

        file_path = os.path.join(app.config['PHOTO_FOLDER'], self.filename)
        rotate(file_path,val)

        file_path=os.path.join(app.config['PHOTO_FOLDER'],self.thumb_filename )
        rotate(file_path,val)

        self.rotate = 0

    def websize(self):
        file_path = os.path.join(app.config['PHOTO_FOLDER'], self.filename)
        im = Image.open(file_path)
        im.thumbnail((400, 400), Image.ANTIALIAS)
        file_path=os.path.join(app.config['PHOTO_FOLDER'],self.thumb_filename )
        im.save(file_path)

    @property
    def thumb_filename(self):
        name = self.filename.split('.')
        return name[0]+'_thumb.'+name[1]


    @classmethod
    def find_by_article_id(cls, id):
        return Photo.query.filter(Photo.post_id == id).order_by(asc(Photo.display_order)).all()

    @classmethod
    def find_by_id(cls, id):
        return Photo.query.filter(Photo.id == id).first()

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @property
    def file_url(self):
        return url_for('static', filename=os.path.join('photos', self.filename))

    @property
    def thumb_file_url(self):
        return url_for('static', filename=os.path.join('photos', self.thumb_filename))

