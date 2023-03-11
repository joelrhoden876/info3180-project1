from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from .config import Config
# import flask migrate here
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here

migrate = Migrate(app, db) 


from app import views