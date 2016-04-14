__author__ = 'johnedenfield'

from flask_wtf import Form
from wtforms import StringField, validators,PasswordField,SubmitField


class LoginForm(Form):
    username = StringField('User Name', [validators.DataRequired("Please enter your username.")])
    password = PasswordField('Password',[validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Login")