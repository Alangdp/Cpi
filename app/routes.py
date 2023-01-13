from app import app
from flask import request, redirect, url_for, render_template, Flask, g, session, make_response, abort
import sqlite3, GetData, fundamentus
from Registro import *
from extras import *
import json, secrets
Acoes = GetData.selecionadosCard()
quantidade = len(Acoes)

@app.route('/home')
def main():
    return render_template('main.html')

@app.route('/', methods=['GET','POST'])
@app.route('/ranking', methods=['GET','POST'])
def ranking():
    return render_template('ranking.html',stock = Acoes, qt = quantidade, user = session['user'])
    
@app.route('/registrar')
def regristrar():
    return render_template('register.html', csrf_token = session['csrfToken'])

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html', csrf_token = session['csrfToken'])


@app.route('/home')
def home():
    return render_template('home.html', user = session['user'])

# valida registros/logins/admin
@app.route('/validar', methods=['GET','POST'])
def validar():
    json_dados = request.get_json()
    print(json_dados)
    if json_dados['action'] == 'registro':
        usuario = json_dados['usuario']
        email = json_dados['email'] 
        senha = json_dados['senha']
        cpf = json_dados['cpf']
        csrf_token = json_dados['csrfToken']

        if not csrf_token == session['csrfToken']: return redirect('registrar', 304)

        if(validaPostR(usuario,email,senha,cpf)):
            registrar(usuario,senha,email,cpf)
            return redirect('/registrar', code=302)
        else:
            return redirect('/registrar', code=304)
    
    if json_dados['action'] == 'login':
        email = json_dados['email']
        senha = json_dados['senha']
        csrf_token = json_dados['csrfToken']

        if not csrf_token == session['csrfToken']: return redirect('registrar', 304)

        if(logar(email, senha)):
            session['logged'] = True
            session['user'] = retornDB(email, senha)
            return redirect(url_for('ranking'))
        else:
            session['logged'] = False
            return redirect('/login', code=304)

    if json_dados['action'] == 'logout':
        session['logged'] = False
        session['user'] = None
        return redirect(url_for('login'))

    if json_dados['action'] == 'admin':
        email = json_dados['email']
        senha = json_dados['senha']

        if email != 'admin@gmail.com' and senha != '(Alant34t)': return make_response(304)
        else:
            session['admin'] = 'True'
            return redirect(url_for('admin'))

    if json_dados['action'] == 'logoutAdmin':
        session['admin'] = 'false'
        return redirect(url_for('admin'))

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    # valida ticker
    ticker = request.args.get('ticker')
    if ticker == None or ticker == '': validTicker =  "False"
    else: 
        validTicker = isTicker(ticker)

    # coleta os dados para a página
    if validTicker == "True":
        stock = GetData.BasicData(ticker)
        datas = stock.Datas()
        tickerImg = stock.getImageDetalhes()
        fundamentalDatas = stock.fundamentalDatas()
        dy = stock.Dy()
        acoesEmitidas = fundamentalDatas['acoesEmitidas'].split('.')
        acoesEmitidas = float(fundamentalDatas['lucroLiquido']) / float(''.join(acoesEmitidas))
        fundamentalDatas['lucroLiquidoPorAcao'] = f'{acoesEmitidas:.2f}'
        print('FundamentalData',fundamentalDatas)
        print('Data',datas)
        print('Dy', dy)

    else:
        dy = []
        datas = []
        fundamentalDatas = []
        tickerImg = []

    return render_template('details.html', user = session['user'], valid = validTicker, ticker = ticker, data = datas, fundamentalData = fundamentalDatas, img = tickerImg, dy = dy)

@app.route('/admin', methods=['GET', 'Post'])
def admin():
    data = usuariosRegistrados()
    return render_template('admin.html', admin = session['admin'], data = data, qtd = len(data), permissoes = "Banido")

@app.route('/error')
def erroPage():
    erro = request.args.get('erro')
    mensagem = request.args.get('mensagem')
    return render_template('errorPage.html', erro = erro , mensagem = mensagem)

# cria a session inicial, caso não exista
@app.before_request
def isFirstLogin():
    if 'logged' in session:
        pass
    else:
        session['logged'] = False
        session['user'] = None
        session['admin'] = False

# verifica se está logado
@app.before_request
def isLogged(*args):
    if request.path.startswith('/static/'):
        return
    if request.path == '/login' or request.path == '/validar' or request.path == '/registrar':
        return
    else:
        if session['logged'] == True:
            return
    if session['logged'] == False:
            return redirect(url_for('login'))

# distribui variaveis pelas páginas
@app.before_request
def reposts(*args):
    if request.path.startswith('/static/'):
        return
    if request.path == '/validar':
        return
    else:
        session['csrfToken'] = secrets.token_hex()
        print(session['csrfToken'])


    

# verifica se ocorreu um erro na conexão
@app.after_request
def check_error(response):
    if response.status_code == 400:
        return redirect('/error?erro=400&mensagem=A%20página%20não%20foi%20carregada%20no%20servidor')
    return response