from app import app
from flask import request, redirect, url_for, render_template, Flask
import sqlite3
import GetData
from Registro import *
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)

@app.route('/')
@app.route('/ranking')
def ranking():
    return render_template('ranking.html',stock = Acoes, qt = quantidade)
    
@app.route('/registrar')
def regristrar():
    return render_template('register.html')

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
    