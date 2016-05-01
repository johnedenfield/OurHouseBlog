__author__ = 'johnedenfield'

from sqlalchemy import desc, func
from app import db

import datetime

class RSVP(db.Model):
    __tablename__ = 'rsvp'
    id = db.Column(db.Integer, primary_key=True)
    attending= db.Column(db.Boolean)
    declining= db.Column(db.Boolean)
    honorific = db.Column(db.String(25))
    name = db.Column(db.String(250))
    number=db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def all(cls):
        return RSVP.query.order_by(desc(RSVP.updated)).all()

    @classmethod
    def number_attending(cls):
        return RSVP.query.with_entities(func.sum(RSVP.number)).filter(RSVP.attending==True).scalar()

    @classmethod
    def find_by_id(cls, id):
        return RSVP.query.filter(RSVP.id == id).first()




