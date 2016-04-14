__author__ = 'johnedenfield'

from flask import render_template, Blueprint,request,make_response,url_for,redirect
from app import db
from app.wedding.forms import RSVPForm, RSVPEditForm
from app.wedding.models import RSVP
from datetime import datetime


wedding = Blueprint('wedding', __name__, template_folder='templates')

@wedding.route('/', methods=['POST','GET'])
def index():

    id = request.cookies.get('User_id')

    print id
    my_rsvp = RSVP.find_by_id(id)

    if my_rsvp:
        form = RSVPEditForm(obj=my_rsvp)

    else:
        form = RSVPForm()

    return render_template('wedding.html',form=form)

@wedding.route('/rsvp', methods=['POST'])
def create_rsvp():
    print(request.form)

    if 'id' in request.form:
        form = RSVPEditForm()
        my_rsvp = RSVP.find_by_id(request.form['id'])
    else:
        form = RSVPForm()
        my_rsvp = RSVP()

    if form.validate_on_submit():

        form.populate_obj(my_rsvp)

        db.session.add(my_rsvp)
        db.session.commit()

        response= make_response(redirect(url_for('wedding.index')))

        expire_date=datetime.strptime('01-1-20','%m-%d-%y')
        response.set_cookie('User_id',value=str(my_rsvp.id), expires=expire_date)
        return response

