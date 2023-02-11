from flask import request, redirect, flash ,url_for, render_template, g, session, make_response
from extras import *

def userIndex():
    # criaAviso('serverMessages', {'email': ['teste da funcao']})
    return render_template('user.html', user = session['user'], csrf_token = session['csrfToken'])