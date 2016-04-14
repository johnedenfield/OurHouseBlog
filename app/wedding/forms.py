__author__ = 'johnedenfield'
from flask_wtf import Form
from wtforms import StringField,BooleanField, HiddenField,IntegerField
from wtforms.validators import DataRequired, NumberRange


class RSVPForm(Form):
    honorific = StringField('Name',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    attending = BooleanField('Attending')
    declining = BooleanField('Decline ')
    number = IntegerField('Number of guests',validators=[DataRequired(),NumberRange(1,2,'Please fill in the number attending')])

class RSVPEditForm(RSVPForm):
    id = HiddenField()