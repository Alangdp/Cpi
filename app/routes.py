from app import app
from flask import request, redirect, url_for, render_template, Flask, g, session, make_response
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
    session['admin'] = 'False'

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

def usuariosRegistrados():
    con = sqlite3.connect('Usuarios.db')
    cur = con.cursor()
    dados = []
    cur.execute("SELECT * FROM usuarios")
    for x in cur:
        dados.append({
            'user': x[0],
            'password': x[1],
            'email': x[2],
            'cpf': x[3],
        })
    return dados
    
usuariosRegistrados()

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
        session.pop('email', 'None')
        session.pop('senha', 'None')
        session['logged'] = False
        session['admin'] = 'false'
        return redirect(url_for('login'))

    if json_dados['action'] == 'admin':
        email = json_dados['email']
        senha = json_dados['senha']
        print(email, senha, session)

        if email != 'admin@gmail.com':
            return make_response(304)
        else:
            if senha != '(Alant34t)':
                return make_response(304)
            else:
                session['admin'] = 'True'
                return redirect(url_for('admin'))
                

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

@app.route('/admin', methods=['GET', 'Post'])
def admin():
    isLogged()
    data = usuariosRegistrados()
    return render_template('admin.html', admin = session['admin'], data = data, qtd = len(data))

