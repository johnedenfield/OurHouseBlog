__author__ = 'johnedenfield'

from flask import render_template, Blueprint,request,make_response,url_for,redirect,flash
from app import db
from app.wedding.forms import RSVPForm, RSVPEditForm
from app.wedding.models import RSVP
from datetime import datetime
from flask_login import login_required,current_user

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

    return render_template('wedding.html',form=form, my_rsvp=my_rsvp,user=current_user)

@wedding.route('/rsvp', methods=['POST'])
def create_rsvp():

    if 'id' in request.form:
        form = RSVPEditForm()
        my_rsvp = RSVP.find_by_id(request.form['id'])

    else:
        form = RSVPForm()
        my_rsvp = RSVP()

    if form.validate_on_submit():

        form.populate_obj(my_rsvp)
        my_rsvp.updated = datetime.now()

        db.session.add(my_rsvp)
        db.session.commit()

        response= make_response(redirect(url_for('wedding.index')))

        expire_date=datetime.strptime('01-1-20','%m-%d-%y')
        response.set_cookie('User_id',value=str(my_rsvp.id), expires=expire_date)

        return response

    return render_template('wedding.html',form=form,user=current_user)

@wedding.route('/montana', methods=['POST','GET'])
def montana():
    return render_template('montana.html')


@wedding.route('/rsvp_list', methods=['POST','GET'])
@login_required
def rsvp_list():
    rsvp = RSVP.all()
    attending =RSVP.number_attending()
    return render_template('rsvp_list.html', rsvp=rsvp, attending=attending)
