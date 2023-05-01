from flask import Flask, current_app
from threading import Thread
from .middlewares import errorsMiddlware, loginMiddlware, spreadMiddlware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask_session import Session
from app.utils.Getdata import BD
from app.utils.carteira import consolidWallet as CW, changeSelicIbov
from app.utils.Threads import atualizaDB
from app import routes
import os, time

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)

routes.init_routes(app)

loginMiddlware.init_app1(app)
spreadMiddlware.init_app(app)
loginMiddlware.init_app2(app)
errorsMiddlware.init_app(app)

def job10Min():
    horaAtual = int(time.strftime('%H'))
    if horaAtual < 11 or horaAtual > 18: return
    BD.variacoes()
    CW([],[],True)
    changeSelicIbov()

def job50Min():
    atualizaDB()

def schedule_jobs():
    with app.app_context():
        executors = {
            'default': ThreadPoolExecutor(16),
            'processpool': ProcessPoolExecutor(4)
        }

        sched = BackgroundScheduler(timezone='America/Sao_Paulo', executors=executors)

        sched.add_job(job10Min, 'interval', seconds=600)
        # sched.add_job(job50Min, 'interval', seconds=3000)

        sched.start()

thread = Thread(target=schedule_jobs)
thread.start()
Session(app)
