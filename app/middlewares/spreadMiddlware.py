from flask import request, redirect, url_for, g, session, flash
from .loginMiddlware import isFirstLogin, init_app1
import secrets

def spread(app):
    @app.before_request
    def _spread():
        if request.method == 'POST':
            return
        g.lockedPaths = ['/login', '/validar', '/registrar', '/testar', '/error', '/home']
        if request.path.startswith('/static/'):
            return 
        
        session['csrfToken'] = secrets.token_hex()
        if 'user' in session and session['user'] and 'logged' in session:
            g.logged = session['logged']
            g.user = session['user'][0][0]
            
def init_app(app):
    spread(app)
    return

