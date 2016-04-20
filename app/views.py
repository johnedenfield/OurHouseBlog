__author__ = 'johnedenfield'

from flask import render_template
from app.login.models import User
from app import app, login_manager
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    # Log in User
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        return user



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', user=current_user)


