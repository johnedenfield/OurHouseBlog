__author__ = 'johnedenfield'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

# configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/houseblog.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTO_FOLDER = os.path.join(APP_ROOT, 'static','photos')

app.config.from_object(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

from app import models
from app import views

