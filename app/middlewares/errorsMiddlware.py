from flask import request, redirect, url_for, g, session
import secrets

# verifica se ocorreu um erro na conexão

def check_error(app):
    @app.after_request
    def _check_error(response):
        if request.path in g.lockedPaths:
            return response
        if 400 <= response.status_code < 600:
            handle_error(response.status_code)
        return response

def init_app(app):
    check_error(app)
    return

def handle_error(status_code):
    session['erro'] = { 'code': status_code, 'message': 'Ocorreu um erro'}
    return redirect('/error')