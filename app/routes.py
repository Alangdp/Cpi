from app import app
from flask import request, redirect, url_for, render_template
import sqlite3
import GetData

Acoes = GetData.getLocalData()
quantidade = len(Acoes)

@app.route('/')
@app.route('/index')
@app.route('/ranking')
def ranking():
    return render_template('ranking.html',stock = Acoes, qt = quantidade)
    
@app.route('/registrar')
def regristrar():
    return render_template('register.html')

@app.route('/autenticar', methods=['GET','POST'])
def autenticar():
    usuario = request.args.get('usuario')
    email = request.args.get('email')
    senha = request.args.get('senha')
    return f'usuario :{usuario} \n email:{email} \n senha:{senha}'

@app.route('/valid', methods=['GET','POST'])
def valid():
    lt = {}
    ticker = request.args.get('ticker')
    ticker.upper()
    stock = GetData.BasicData(ticker)
    lt['name'] = stock.Datas()['name'],
    lt['value'] = stock.Datas()['value'],
    lt['dy_porcent'] = stock.Datas()['dy_porcent'],
    lt['dy6'] = stock.Dy()['dy6'],
    lt['margin'] = stock.Margin(),
    lt['ranking'] = 1,
    lt['img'] = stock.getImage()

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    lt = {}
    ticker = request.args.get('ticker')
    ticker.upper()
    stock = GetData.BasicData(ticker)
    return render_template('details.html', infos = stock.Datas(), sinfo = stock.fundamentalDatas(), infosBB = stock.buyBack())
    

    


# @app.route('/test')
# def test():
#     return render_template('teste.html',stock = Acoes, qt = quantidade)
                        