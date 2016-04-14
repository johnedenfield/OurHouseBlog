__author__ = 'johnedenfield'

from flask_wtf import Form
from wtforms import StringField, TextAreaField, \
    BooleanField, FileField,HiddenField,IntegerField, SelectField

class ArticleCreateForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
    posted = BooleanField('Post')
    post_order = IntegerField('Post Order')

class ArticleEditForm(ArticleCreateForm):
    id = HiddenField()

class PhotoForm(Form):
    post_id = HiddenField()
    file = FileField('Photo')


class PhotoEditForm(PhotoForm):
    id = HiddenField()
    caption = TextAreaField('Caption')
    display_order = IntegerField('Display Order')
    rotate = SelectField(u'Rotate', choices=[('0', '0 deg' ),('90', '90 deg' ), ('180', '180 deg' ), ('270', '270 deg')])

