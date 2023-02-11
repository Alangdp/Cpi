from flask import Flask
from .middlewares import errorsMiddlware, loginMiddlware, spreadMiddlware
from flask_session import Session
from app import routes
import os


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)

routes.init_routes(app)

loginMiddlware.init_app1(app)
spreadMiddlware.init_app(app)
loginMiddlware.init_app2(app)
errorsMiddlware.init_app(app)

Session(app)
