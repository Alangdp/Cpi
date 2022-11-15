from app import app
from flask import request, redirect, url_for, render_template, Flask
import sqlite3
import GetData
from Registro import *
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)

def validaDiferença(senha, email):
    if(senha == None or email == None):
        senha = request.cookies.get('senha')
        email = request.cookies.get('email')

    return email,senha

@app.route('/', methods=['GET','POST'])
@app.route('/ranking', methods=['GET','POST'])
def ranking():

    email = request.form.get("email")
    senha  = request.form.get("senha")
    senhas_cookie = validaDiferença(senha, email)

    print(logar(senhas_cookie[0], senhas_cookie[1]))
    if not logar(senhas_cookie[0], senhas_cookie[1]):
        return render_template('login.html')
    
    user = retornDB(senhas_cookie[0], senhas_cookie[1])
    return render_template('ranking.html',stock = Acoes, qt = quantidade, user = user)
    
@app.route('/registrar')
def regristrar():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST','POST'])
def autenticar():
    usuario = request.form.get('usuario')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cpf = request.form.get('cpf')
    registrar(usuario,senha,email,cpf)

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    lt = {}
    ticker = request.args.get('ticker')
    ticker.upper()
    stock = GetData.BasicData(ticker)
    return render_template('details.html', infos = stock.Datas(), sinfo = stock.fundamentalDatas(), infosBB = stock.buyBack())
    