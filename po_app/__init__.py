from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'bB0Fd805FeC_w)Lp&)UDJQ5£'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'po_app.db')
app.config['STATIC_PATH'] = os.environ.get('ENV_STATIC_PATH') or app.root_path

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from po_app import routes, models
