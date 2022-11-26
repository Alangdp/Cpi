from app import app
from flask import request, redirect, url_for, render_template, Flask, g, session
import sqlite3
import GetData
from Registro import *
import json
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)

def baseSession():
    session['email'] = 'none'
    session['senha'] = 'none'
    session['logged'] = False



def isLogged():
    try:
        email = session['email']
        senha = session['senha']
        user = retornDB(email, senha)

        if 'logged' in session:
            if session['logged'] == True:
                return True, user
            else:
                return False, user

        else:
            return False, user
    except:
        baseSession()
        return None, None
        
@app.route('/', methods=['GET','POST'])
def main():
    return render_template('main.html')

@app.route('/ranking', methods=['GET','POST'])
def ranking():
    info = isLogged()
    if info[0]:
        return render_template('ranking.html',stock = Acoes, qt = quantidade, user = info[1])
    else:
        return redirect(url_for('login'))
    
@app.route('/registrar')
def regristrar():
        return render_template('register.html', )

@app.route('/validar', methods=['GET','POST'])
def validar():
    json_dados = request.get_json('usuario')
    if json_dados['action'] == 'registro':
        usuario = json_dados['usuario']
        email = json_dados['email'] 
        senha = json_dados['senha']
        cpf = json_dados['cpf']

        if(validaPostR(usuario,email,senha,cpf)):
            registrar(usuario,senha,email,cpf)
            return redirect('/registrar', code=302)
        else:
            return redirect('/registrar', code=304)
    
    if json_dados['action'] == 'login':
        if 'email' in session:
            session.pop('email', None)
        if 'senha' in session:
            session.pop('senha', None)
        email = json_dados['email']
        senha = json_dados['senha']
        if(validaPostL(email, senha)):
            if(logar(email, senha)):
                session['email'] = email
                session['senha'] = senha
                session['logged'] = True
                return redirect(url_for('ranking'))
            else:
                session['logged'] = False
                return redirect('/login', code=304)
        else:
            return redirect('/registrar', code=304)

    if json_dados['action'] == 'logout':
        print('teste')
        session.pop('email', 'None')
        session.pop('senha', 'None')
        session['logged'] = False
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')
    

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    info = isLogged()
    if info[0] == True:
        return render_template('details.html',user = info[1])
    else:
        return redirect(url_for('login'))

