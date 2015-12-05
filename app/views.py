__author__ = 'johnedenfield'

from models import Article, Photo, User
from flask import render_template, request, session, url_for, redirect, flash
from forms import ArticleCreateForm, ArticleUpdateForm, PhotoForm,PhotoUpdateForm,LoginForm
from werkzeug.utils import secure_filename
from app import app, db, login_manager
from flask_login import login_required, login_user, logout_user, current_user

import os


@login_manager.user_loader
def load_user(user_id):
    # Log in User
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        return user

@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404

@app.route('/')
def index():
    articles = Article.all()
    return render_template('index.html', articles=articles, user=current_user)

@app.route('/article/<int:id>/<slug>')
def show_article(id, slug):
    article = Article.find_by_id(id)
    photos = Photo.find_by_article_id(id)

    return render_template('show_article.html', article=article, photos=photos, user =current_user)
@app.route('/goto/<int:id>')
def goto_article(id):
    article = Article.find_by_id(id)
    if article:
        return redirect(url_for('show_article',id=article.id,slug=article.slug))
    return redirect(url_for('index'))

@app.route('/article_create', methods=['GET', 'POST'])
@login_required
def article_create():

    article = Article()
    form = ArticleCreateForm()

    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_article.html', form=form, article=article)



@app.route('/article/<int:id>/<slug>/edit', methods=['GET', 'POST'])
@login_required
def article_update(id, slug):
    article = Article.find_by_id(id)
    photos=Photo.find_by_article_id(id)

    if not article:
        return HTTPNotFound(404)
    form = ArticleUpdateForm(request.form, article)

    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_article.html', form=form, article=article, photos=photos)


@app.route('/article/<int:id>/<slug>/delete', methods=['GET', 'POST'])
@login_required
def article_delete(id, slug):

    article = Article.find_by_id(id)
    if not article:
        return HTTPNotFound(404)

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/upload/<int:id>', methods=['GET', 'POST'])
@login_required
def upload_photo(id):

    photo=Photo()
    form = PhotoForm()
    # Set hidden field to post_id
    form.post_id.data = id

    if form.validate_on_submit():

        file = request.files['file']
        file.filename = str(id) +"_" + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))

        form.populate_obj(photo)
        photo.filename =file.filename
        db.session.add(photo)
        db.session.commit()

        article = Article.find_by_id(id)

        return redirect(url_for('show_article',id=id, slug =article.slug))


    return render_template('photo.html', form=form)

@app.route('/photo/<int:id>', methods=['GET', 'POST'])
@login_required
def update_photo(id):

    photo=Photo.find_by_id(id)

    if not photo:
        return HTTPNotFound(404)
    form = PhotoUpdateForm(request.form, photo)

    if form.validate_on_submit():
        form.populate_obj(photo)
        db.session.add(photo)
        db.session.commit()
        article = Article.find_by_id(photo.post_id)
        return redirect(url_for('article_update', id=article.id, slug= article.slug))

    return render_template('update_photo.html', form=form )


@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
