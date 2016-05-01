__author__ = 'johnedenfield'

from flask import render_template, request, url_for, redirect,Blueprint
from app.webhelpers import HTTPNotFound
from models import Article, Photo
from forms import ArticleCreateForm, ArticleEditForm, PhotoForm, PhotoEditForm
from app import db

from flask_login import login_required,current_user
from sqlalchemy import desc, asc

house = Blueprint('house', __name__,template_folder='templates')

@house.route('/')
def all_articles():
    articles = Article.all()
    return render_template('all_articles.html', articles=articles, user=current_user)


@house.route('/article/<int:id>')
def article_show(id):
    article = Article.find_by_id(id)
    photos = Photo.find_by_article_id(id)

    return render_template('article.html', article=article, photos=photos, user=current_user)


@house.route('/goto/<int:id>/<direction>')
def article_goto(id, direction):
    if direction == 'forward':
        article = Article.query.filter(Article.post_order > id).order_by(asc(Article.post_order)).first()
    else:

        article = Article.query.filter(Article.post_order < id).order_by(desc(Article.post_order)).first()

    if article:
        return redirect(url_for('house.article_show', id=article.id))
    return redirect(url_for('house.all_articles'))


@house.route('/article_create', methods=['GET', 'POST'])
@login_required
def article_create():
    article = Article()
    form = ArticleCreateForm()
    form.post_order.data = db.session.query(db.func.max(Article.post_order)).scalar()+1

    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('house.article_show', id=article.id))
    return render_template('article_create.html', form=form, article=article)


@house.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    article = Article.find_by_id(id)
    photos = Photo.find_by_article_id(id)

    if not article:
        return HTTPNotFound()

    form = ArticleEditForm(request.form, article)

    if form.validate_on_submit():
        form.populate_obj(article)

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('house.article_show', id=article.id))
    return render_template('article_edit.html', article=article, photos=photos, form=form)




@house.route('/article/<int:id>/delete', methods=['GET', 'POST'])
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

    return redirect(url_for('house.all_articles'))


@house.route('/article/<int:post_id>/photo_create', methods=['GET', 'POST'])
@login_required
def photo_create(post_id):
    form = PhotoForm()
    form.post_id.data = post_id

    if form.validate_on_submit():
        files = request.files.getlist('file')

        for file in files:
            photo = Photo()
            photo.upload(file, post_id)

        return redirect(url_for('house.article_show', id=post_id))

    return render_template('photo_create.html', form=form)


@house.route('/photo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def photo_edit(id):
    photo = Photo.find_by_id(id)

    if not photo:
        return HTTPNotFound(404)

    form = PhotoEditForm(request.form, photo)

    if form.validate_on_submit():
        form.populate_obj(photo)
        angle = float(form.rotate.data)
        photo.rotate_photo(angle)

        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('house.article_edit', id=photo.post_id))

    return render_template('photo_edit.html', form=form, photo=photo)


@house.route('/photo/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def photo_delete(id):
    photo = Photo.find_by_id(id)
    photo.delete()

    return redirect(url_for('house.article_edit', id=photo.post_id))


@house.route('/floorplan', methods=['GET', 'POST'])
def floor_plan():

    return render_template('floor_plan.html')