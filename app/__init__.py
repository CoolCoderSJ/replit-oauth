import os
import flask
from flask_session import Session
from s1db import S1

app = flask.Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from .routes import *