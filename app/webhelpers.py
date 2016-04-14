__author__ = 'johnedenfield'
from flask import render_template
from app import app

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
