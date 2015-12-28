__author__ = 'johnedenfield'

from flask_wtf import Form
from wtforms import StringField, validators, TextAreaField, \
    PasswordField,SubmitField,BooleanField, FileField,HiddenField,IntegerField, SelectField

class ArticleCreateForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
    posted = BooleanField('Post')

class ArticleUpdateForm(ArticleCreateForm):
    id = HiddenField()

class PhotoForm(Form):
    post_id = HiddenField()
    file = FileField('Photo')


class PhotoUpdateForm(PhotoForm):
    id = HiddenField()
    caption = TextAreaField('caption')
    display_order = IntegerField('Display Order')
    rotate = SelectField(u'Rotate', choices=[('0 Deg', 0 ),('90 Deg', 90 ), ('180 Deg', 180 ), ('270 Deg', 270)])

class LoginForm(Form):
    username = StringField('User Name', [validators.DataRequired("Please enter your username.")])
    password = PasswordField('Password',[validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Login")