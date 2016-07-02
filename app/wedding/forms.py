__author__ = 'johnedenfield'
from flask_wtf import Form
from wtforms import StringField,BooleanField, HiddenField,IntegerField
from wtforms.validators import DataRequired, NumberRange


class RSVPForm(Form):
    honorific = StringField('Name') # Not in use. Use Name field only
    name = StringField('Name',validators=[DataRequired(message="Please enter you and your guests name ")])
    attending = BooleanField('Attending')
    declining = BooleanField('Decline ')
    number = IntegerField('Number of guests',validators=[DataRequired(),NumberRange(0,2,'Please let us know the the total number attending')])

class RSVPEditForm(RSVPForm):
    id = HiddenField()