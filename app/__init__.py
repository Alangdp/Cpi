from flask import Flask, current_app
from .middlewares import errorsMiddlware, loginMiddlware, spreadMiddlware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_session import Session
from app.utils.Getdata import BD
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

with app.app_context():
    executors = {
        'default': ThreadPoolExecutor(16),
        'processpool': ProcessPoolExecutor(4)
    }

    sched = BackgroundScheduler(timezone='America/Sao_Paulo', executors=executors)

    sched.add_job(BD.variacoes(), 'interval', seconds=600)
    sched.start()

Session(app)
