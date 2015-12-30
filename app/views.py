__author__ = 'johnedenfield'

from models import Article, Photo, User
from flask import render_template, request, url_for, redirect, flash
from forms import ArticleCreateForm, ArticleEditForm, PhotoForm, PhotoEditForm, LoginForm
from app import app, db, login_manager
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc, asc


@login_manager.user_loader
def load_user(user_id):
    # Log in User
    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        return user


@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def index():
    articles = Article.all()
    return render_template('index.html', articles=articles, user=current_user)


@app.route('/article/<int:id>')
def article_show(id):
    article = Article.find_by_id(id)
    photos = Photo.find_by_article_id(id)

    return render_template('article.html', article=article, photos=photos, user=current_user)


@app.route('/goto/<int:id>/<direction>')
def article_goto(id, direction):
    if direction == 'forward':
        article = Article.query.filter(Article.post_order > id).order_by(asc(Article.post_order)).first()

    else:

        article = Article.query.filter(Article.post_order < id).order_by(desc(Article.post_order)).first()


    if article:
        return redirect(url_for('article_show', id=article.id))
    return redirect(url_for('index'))


@app.route('/article_create', methods=['GET', 'POST'])
@login_required
def article_create():
    article = Article()
    form = ArticleCreateForm()
    form.post_order.data = db.session.query(db.func.max(Article.post_order)).scalar()+1

    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('article_show', id=article.id))
    return render_template('article_create.html', form=form, article=article)


@app.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    article = Article.find_by_id(id)
    photos = Photo.find_by_article_id(id)

    if not article:
        return HTTPNotFound(404)
    form = ArticleEditForm(request.form, article)

    if form.validate_on_submit():
        form.populate_obj(article)

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article_show', id=article.id))
    return render_template('article_edit.html', article=article, photos=photos, form=form)


@app.route('/article/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def article_delete(id):
    article = Article.find_by_id(id)
    if not article:
        return HTTPNotFound(404)

    photos = Photo.find_by_article_id(id)
    for photo in photos:
        photo.delete()

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/article/<int:post_id>/photo_create', methods=['GET', 'POST'])
@login_required
def photo_create(post_id):
    form = PhotoForm()
    form.post_id.data = post_id

    if form.validate_on_submit():
        files = request.files.getlist('file')

        for file in files:
            photo = Photo()
            photo.upload(file, post_id)

        return redirect(url_for('article_show', id=post_id))

    return render_template('photo_create.html', form=form)


@app.route('/photo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def photo_edit(id):
    photo = Photo.find_by_id(id)

    if not photo:
        return HTTPNotFound(404)

    form = PhotoEditForm(request.form, photo)

    if form.validate_on_submit():
        form.populate_obj(photo)
        angle = 360 - float(form.rotate.data)
        if angle > 0:
            photo.rotate_photo(angle)

        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('article_edit', id=photo.post_id))

    return render_template('photo_edit.html', form=form, photo=photo)


@app.route('/photo/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def photo_delete(id):
    photo = Photo.find_by_id(id)
    photo.delete()

    return redirect(url_for('article_edit', id=photo.post_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = User.query.filter(User.username == form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            print user
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
