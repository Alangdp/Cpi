from app import app
from flask import request, redirect, url_for, render_template, Flask
from flask_session import Session
import sqlite3
import GetData
from Registro import *
import json
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)


def validaDiferença(senha = None, email = None):
    if(senha == None or email == None):
        senha = request.cookies.get('senha')
        email = request.cookies.get('email')

    return email,senha

def isLogged():
    senhas_cookie = validaDiferença()

    email = senhas_cookie[0]
    senha = senhas_cookie[1]
    user = retornDB(senhas_cookie[0], senhas_cookie[1])

    if not logar(senhas_cookie[0], senhas_cookie[1]):
        return False , user
    else:
        return True ,  user
        
@app.route('/', methods=['GET','POST'])
def main():
    return render_template('main.html')

@app.route('/ranking', methods=['GET','POST'])
def ranking():
    par = isLogged()
    if not par[0]:
        return redirect(url_for('login'))
    else:
        return render_template('ranking.html',stock = Acoes, qt = quantidade, user = par[1])
    
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
        email = json_dados['email']
        senha = json_dados['senha']

        if(validaPostL(email, senha)):
            if(logar(email, senha)):
                return redirect('/registrar', code=302)
            else:
                return redirect('/registrar', code=304)
        else:
            return redirect('/registrar', code=304)

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')
    

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    par = isLogged()
    if not par[0]:
        return render_template('login.html')
    else:
        return render_template('details.html',user = par[1])

