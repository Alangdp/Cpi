from flask import request, redirect, flash ,url_for, render_template, g, session, make_response, current_app
import sqlite3, fundamentus, requests, json, sys ,app.utils.Getdata as Getdata, json
from app.utils.carteira import comandoSQL as carteiraSQL
from Registro import comandoSQL as comandoUsuarios
from newsapi import NewsApiClient
from Registro import *
sys.path.append('..')

from app.utils.extras import *
from app.utils.carteira import *

import numpy as np

newsapi = NewsApiClient(api_key='5e13fe6018a14877aca173ff6688260b')

# Controllers
Acoes = Getdata.selected()
quantidade = len(Acoes)

def routes(app):

    @app.route('/teste')
    def teste():
        return render_template('teste.html')

    @app.route('/')
    @app.route('/home')
    def main():
        listaDeImagens = []
        noticiaF = []
        variacoes = []
        noticias = newsapi.get_everything(q='bolsa brasileira',language='pt',sort_by='relevancy')
        if not noticias['status'] == 'ok': return render_template('home.html', noticias = noticiaF)
        for noticia in noticias['articles']:
            if noticia['urlToImage'] in listaDeImagens: continue
            listaDeImagens.append(noticia['urlToImage'])
            noticiaF.append({
                'titulo': noticia['title'],
                'descricao': noticia['description'],
                'url-image': noticia['urlToImage'],
                'url': noticia['url'],})
            if len(noticiaF) >= 6: break

        with open('./app/json/homeVar.json', 'r') as file:
            variacoes.append(json.load(file))

        # for x in variacoes[0]:
        #     print()
        #     for y in x:
        #         print(y)
        return render_template('home.html', noticias = noticiaF, variacoes = variacoes[0])

    @app.route('/ranking', methods=['GET','POST'])
    def ranking():
        return render_template('ranking.html',stock = Acoes, qt = quantidade, user = session['user'])

    # Registro
    @app.route('/registrar', methods=['GET'])
    def registrarIndex():
        return render_template('register.html', csrf_token = session['csrfToken'])

    @app.route('/registrar', methods=['POST'])
    def registrar():
        json_dados = request.get_json()
        if validaCSR(json_dados['csrfToken']):
            user = json_dados['usuario']
            email = json_dados['email']
            senha = json_dados['senha']
            cpf = json_dados['cpf']
            if registrarDB(user,senha,email,cpf):
                return redirect('/login', code=302)
            return redirect('/registrarIndex', code=302)
        else:
            return redirect('/registrarIndex', code=304)

    #Login/Logout
    @app.route('/login', methods=['GET'])
    def loginPage():
        print(session['csrfToken'])
        return render_template('login.html', csrf_token = session['csrfToken'])

    @app.route('/login', methods=['POST'])
    def login():
        json_dados = request.get_json()
        if json_dados['action'] == 'login' and validaCSR(json_dados['csrfToken']):
            email = json_dados['email']
            senha = json_dados['senha']

            if logar(email, senha): return redirect('/ranking', code=302)
            else: return redirect(url_for('loginPage'), code=304)
        return redirect(url_for('loginPage'), code=304)

    @app.route('/logout', methods=['POST'])
    def logout():
        session['logged'] = 'False'
        session['user'] = None
        return redirect('login')

    @app.route('/home')
    def home():
        return render_template('home.html', user = session['user'])

    @app.route('/user', methods=['POST'])
    def userConfig():
        form = request.form
        if form['action'] == 'password':
            atualizarSenha(form['inputPasswordN'], form['inputPasswordA'], form['id'])
            return redirect('/user')
        if form['action'] == 'email':
            atualizarEmail(form['inputEmailN'], form['inputEmailA'],  form['id'] )
        return redirect('/user')

    @app.route('/user', methods=['GET'])
    def userIndexR():
        return render_template('user.html', user = session['user'], csrf_token = session['csrfToken'])

    @app.route('/detalhes', methods=['GET','POST'])
    def detalhes():
        # valida ticker
        ticker = request.args.get('ticker')
        if ticker == None or ticker == '': validTicker =  "False"
        else: validTicker = isTicker(ticker)

        # coleta os dados para a página
        if validTicker == "True":
            stock = Getdata.BD(ticker)
            datas = stock.datas()
            tickerImg = stock.getImageDetalhes()
            fundamentalDatas = stock.fundamentalDatas()
            dy = stock.dy()
            acoesEmitidas = str(fundamentalDatas['acoesEmitidas']).split('.')
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

    # Admin
    @app.route('/admin', methods=['GET', 'Post'])
    def admin():
        if request.method == 'POST':
            json_dados = request.get_json()

            if json_dados['action'] == 'admin':
                email = json_dados['email']
                senha = json_dados['senha']

                if email != 'admin@gmail.com' and senha != '(Alant34t)': return make_response(304)
                else:
                    session['admin'] = 'True'
                    return redirect(url_for('admin'))

            if json_dados['action'] == 'logoutAdmin':
                session['admin'] = 'False'
                return redirect(url_for('admin'))

        else:
            data = usuariosRegistrados()
            return render_template('admin.html', admin = session['admin'], data = data, qtd = len(data), permissoes = "Banido")

    @app.route('/error')
    def erroPage():
        { 'code': 'CSRFToken Inválido', 'message': 'CSRFToken Inválido'}
        erro = session['erro']['code']
        mensagem = session['erro']['message']

        return render_template('errorPage.html', erro = erro , mensagem = mensagem)

    @app.route('/carteira', methods=['GET'])
    @app.route('/carteira/dashboard', methods=['GET'])
    def dashboard():
        ticker = 'BBAS3'.upper()
        updateWallet(ticker, 300, 100, 5)
        return render_template('stockwallet.html')

    @app.route('/db/')
    @app.route('/db/index')
    def indexDB():
        dados = []
        comandos_sql = ['SELECT * FROM carteira_consolidada WHERE id_usuario = ?',
                        'SELECT * FROM carteira_transacoes WHERE id_usuario = ?',
                        'SELECT * FROM carteira_usuario WHERE id_usuario = ?',
                        ]

        argumentos_sql = [(session['id'],),
                      (session['id'],),
                      (session['id'],),
                    ]

        # ticker = 'BBAS3'
        # quantidade = 50
        # valor = 39.11
        # updateWallet(ticker, quantidade, valor, 3)
        porcentWallet()

        dados = consolidWallet(comandos_sql, argumentos_sql)
        return json.dumps(dados)

    @app.route('/db/addn/acao=<ticker>&quantidade=<quantidade>&valor=<valor>', methods=['GET'])
    def adicionarPosicao(ticker, quantidade, valor):
        quantidade = int(quantidade)

        updateWallet(ticker, quantidade, valor, 3)

        return indexDB()

    @app.route('/db/add/acao=<ticker>&quantidade=<quantidade>&valor=<valor>', methods=['GET'])
    def adicionar(ticker, quantidade, valor):

        updateWallet(ticker, quantidade, valor, 1)

        return indexDB()


    @app.route('/db/rem/acao=<ticker>&quantidade=<quantidade>&valor=<valor>', methods=['GET'])
    def remover(ticker, quantidade, valor):
        quantidade = int(quantidade)

        updateWallet(ticker, quantidade, valor, 4)

        return indexDB()


    @app.route('/db/apa/acao=<ticker>&quantidade=<quantidade>&valor=<valor>', methods=['GET'])
    def deletar(ticker, quantidade, valor):
        quantidade = int(quantidade)

        updateWallet(ticker, quantidade, valor, 2)

        return indexDB()


def init_routes(app):
    routes(app)

