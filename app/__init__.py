from flask import Flask
from flask_session import Session

import os
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.secret_key = os.urandom(24)

Session(app)
from app import routes