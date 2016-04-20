__author__ = 'johnedenfield'


from flask import render_template, request, url_for, redirect, flash,Blueprint
from flask_login import login_user, logout_user

from app.login.models import User
from app.login.forms import LoginForm
from app import app




@app.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = User.query.filter(User.username == form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))

        else:
            if user is None:
                flash('User\'s name not found', 'login')
            else:
                flash('Incorrect Password', 'login')

            return render_template('login.html', form=form)

    else:
        return render_template('login.html', form=form)


@app.route("/logout", methods=['GET'])
def log_user_out():
    logout_user()
    return redirect(url_for('log_user_in'))
