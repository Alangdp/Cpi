from flask import request, redirect, url_for, g, session
import secrets 
import app.utils.extras as extras


# cria a session inicial, caso não exista
def isFirstLogin(app):
    @app.before_request
    def _isFirstLogin():
        g.lockedPaths = ['/login', '/validar', '/registrar', '/testar', '/error', '/', '/home']

        if 'logged' in session:
            return
        else:
            session['ipAdress'] = request.remote_addr
            session['logged'] = False
            session['user'] = 'None'
            session['admin'] = False
            return
    
def init_app1(app):
    isFirstLogin(app)
    return

def isLogged(app):
    @app.before_request
    def _isLogged():
        g.lockedPaths = ['/login', '/validar', '/registrar', '/testar', '/error', '/', '/home']
        if request.path.startswith('/static/'):
            return 
        if request.path in g.lockedPaths:
            return 
        if 'logged' in session and session['logged'] == True:
            return 
        return redirect('/login')

def init_app2(app):
    isLogged(app)
    return
