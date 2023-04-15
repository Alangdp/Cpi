import sqlite3, datetime, fundamentus, statistics, requests, requests_cache
from flask import session
from app.utils.extras import isTicker as validaTicker
from app.utils.Getdata import sqlString
import pandas as pd, json

def fundamentaRaw(ticker=''):
    url = 'http://fundamentus.com.br/detalhes.php?papel={}'.format(ticker)
    hdr = {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
        'Accept-Encoding': 'gzip, deflate',
    }

    with requests_cache.enabled():
        content = requests.get(url, headers=hdr)
    
    tables = pd.read_html(content.text, decimal=',', thousands='.')
    df = tables[0]
    return df

path = 'app/database/Carteira.db'
def criaDB():

    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_transacoes (
        id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        quantidade DECIMAL(10,2) NOT NULL,
        preço_unitario DECIMAL(10,5) NOT NULL,
        tipo VARCHAR(15) NOT NULL,
        transacao VARCHAR(15) NOT NULL,
        data_transacao DATE NOT NULL
        );
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_usuario (
        id_usuario INTEGER NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        nome VARCHAR(70) NOT NULL,
        quantidade DECIMAL(10, 0) NOT NULL,
        data_transacao DATE NOT NULL,
        preco_medio DECIMAL(10,2),
        tipo VARCHAR(15),
        PRIMARY KEY (id_usuario, ticker)
        );
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_variacao (
        data DATE NOT NULL,
        id_usuario INTEGER NOT NULL PRIMARY KEY,
        variacao VARCHAR(10),
        valorCarteira DECIMAL(10,2)
        );
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_consolidada (
        id_usuario INTEGER NOT NULL PRIMARY KEY,
        valor DECIMAL(10,2) NOT NULL,
        lucro_prejuizo DECIMAL(10,2),
        variacao VARCHAR(10)
        );
    ''')
    
    con.close()
     
criaDB()

def comandoSQL(comandos: list, argumentos: list):
    retornar = []
    con = sqlite3.connect(path)
    cur = con.cursor()

    for comando, argumento in zip(comandos,argumentos):

        cur.execute(comando, argumento)
        if cur.description:
            retornar.append(cur.fetchall())
        else:
            con.commit()

        ultimoComando = comando
    con.close()
    
    return retornar

def porcentWallet():
    carteira = comandoSQL(['SELECT * FROM carteira_usuario WHERE id_usuario = ?' ], [(session['id'],)])[0]
    valorTotal = 0
    porcent = {'valorTotal': 0, 'Acao': [0, 0, 0, {}], 'Fii': [0, 0, 0, {}] }

    for ativo in carteira:
        ticker = ativo[1]
        quantidade = ativo[3]
        tipo = ativo[6]

        if tipo == 'Fii':
            df = fundamentaRaw(ticker)
            cotacaoAtual = float(df[3][0])
            porcent['Fii'][0] += round((quantidade * cotacaoAtual), 2)
            porcent['Fii'][1] += quantidade
            
        if tipo == 'Acao':
            cotacaoAtual = float(fundamentus.get_papel(ticker)['Cotacao'].iloc[0])
            porcent['Acao'][0] += round((quantidade * cotacaoAtual), 2)
            porcent['Acao'][1] += quantidade

        porcent['valorTotal'] += round((quantidade * cotacaoAtual), 2)

    for ativo in carteira:
        ticker = ativo[1]
        tipo = ativo[6]
        quantidade = ativo[3]

        if tipo == 'Fii':
            df = fundamentaRaw(ticker)
            cotacaoAtual = float(df[3][0])
            valorTotalAtivo = round(quantidade * cotacaoAtual, 2)
            porcent['Fii'][3][ticker] = {'valor': valorTotalAtivo, 'porcentagem': round(valorTotalAtivo / porcent['Fii'][0] * 100, 2)}
            
        if tipo == 'Acao':
            df = fundamentaRaw(ticker)
            cotacaoAtual = float(fundamentus.get_papel(ticker)['Cotacao'].iloc[0])
            valorTotalAtivo = round(quantidade * cotacaoAtual, 2)
            porcent['Acao'][3][ticker] = {'valor': valorTotalAtivo, 'porcentagem': round(valorTotalAtivo / porcent['Acao'][0] * 100, 2)}
        
    for chave in porcent:
        if chave == 'valorTotal': continue
        try:
            porcent[chave][2] = round((porcent[chave][0] / porcent['valorTotal']) * 100, 2)
        except ZeroDivisionError:
            porcent[chave][2] = 0

    print(porcent)
    return porcent

def consolidWallet(comands = [], arguments = [], All = False):
    dataAcao = datetime.date.today().strftime('%Y-%m-%d')
    comandos = []
    argumentos = []
    acoes = {}
    LIDS = [] # Last Ids

    All = True
    if All == True:
        transacoes = comandoSQL(['SELECT * FROM carteira_transacoes'],[()])
    else: 
        transacoes = comandoSQL(['SELECT * FROM carteira_transacoes WHERE id_usuario = ?'],[(session['id'],),])
    
    for transacao in transacoes[0]:
        Id = transacao[1]
        LIDS.append(Id)
        ticker = transacao[2]
        quantidade = transacao[3]
        preco = transacao[4]
        tipo = transacao[6]

        if not Id in acoes:
            acoes[Id] = {}


        if not acoes[Id].__contains__(ticker): 
            if tipo == 'Fii':
                df = fundamentaRaw(ticker)
                cotacaoAtual = float(df[3][0])
                
            if tipo == 'Acao':
                cotacaoAtual = float(fundamentus.get_papel(ticker)['Cotacao'].iloc[0])
            acoes[Id][ticker] = {'quantidade': 0, 'patrimonio': 0, 'valorAcao': cotacaoAtual}
        
        if transacao[5] == 'VENDA' or transacao[5] == 'VENDA COMPLETA': 
            quantidade = quantidade * -1

        acoes[Id][ticker]['quantidade'] += quantidade
        acoes[Id][ticker]['patrimonio'] += (preco * quantidade)

        try:
            acoes[Id][ticker]['precoMedio'] = acoes[Id][ticker]['patrimonio'] / acoes[Id][ticker]['quantidade']
        except ZeroDivisionError:
            acoes[Id][ticker]['precoMedio'] = 0

        precoMedio = float(f"{acoes[Id][ticker]['precoMedio']:.2f}")

        if cotacaoAtual > precoMedio:
            acoes[Id][ticker]['lucro_preju'] = f"{(cotacaoAtual - precoMedio) * int(acoes[Id][ticker]['quantidade']):.2f}" 
        else:
            acoes[Id][ticker]['lucro_preju'] = f"{(precoMedio - cotacaoAtual) * int(acoes[Id][ticker]['quantidade']):.2f}"
        
        try:
            acoes[Id][ticker]['variacao'] = f'{(cotacaoAtual - precoMedio) / precoMedio * 100:.2f}%'
        except ZeroDivisionError:
            acoes[Id][ticker]['variacao'] = '0%'

    LIDS = list(set(LIDS))

    for Id in LIDS:

        for ticker in acoes[Id]:
            comandos.append("UPDATE carteira_usuario SET preco_medio = ? WHERE id_usuario = ? AND ticker = ?")
            argumentos.append((acoes[Id][ticker]['precoMedio'], Id, ticker,))

            acoes[Id][ticker]['valorTotal'] = 0
            acoes[Id][ticker]['lucroTotal'] = 0
            acoes[Id][ticker]['variacaoTotal'] = 0
            
        for ticker in acoes[Id]:

            acoes[Id][ticker]['variacaoTotal'] += float(acoes[Id][ticker]['variacao'].replace('%', ''))
            acoes[Id][ticker]['lucroTotal'] += float(acoes[Id][ticker]['lucro_preju'])
            acoes[Id][ticker]['valorTotal'] += float(acoes[Id][ticker]['valorAcao'] * acoes[Id][ticker]['quantidade'])

        for ticker in acoes[Id]:
            comandos.append("UPDATE carteira_consolidada SET valor = ? ,lucro_prejuizo = ? , variacao = ? WHERE id_usuario = ?")
            argumentos.append((acoes[Id][ticker]['valorTotal'], acoes[Id][ticker]['lucroTotal'], acoes[Id][ticker]['variacaoTotal'], Id,))

            comandos.append("INSERT OR REPLACE INTO carteira_variacao (data, id_usuario, variacao, valorCarteira) SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM carteira_variacao WHERE data = ? AND id_usuario = ?)")
            argumentos.append((dataAcao, Id, acoes[Id][ticker]['variacaoTotal'], acoes[Id][ticker]['valorTotal'], dataAcao, Id,))

    if len(comands) > 0:
        comandos.extend(comands)
        argumentos.extend(arguments)

    dados = comandoSQL(comandos, argumentos)

    return dados

def updateWallet(ticker = '', quantidade = 0, valor = 0, code = 1 , tipo = 'Acao'):
    dataTransacao = datetime.date.today().strftime('%Y-%m-%d')
    df = ''
    if quantidade <= 0: return
    if code < 3 and code > 0: 
        if not validaTicker(ticker): return

    stockInfo = fundamentus.get_papel(ticker)

    if tipo == 'Fii':
        df = fundamentaRaw(ticker)
        nome = df[1][1]

    else: nome = stockInfo['Empresa'].iloc[0]

    if code == 1:
        comandoSQL(  
            [
            "UPDATE carteira_usuario SET quantidade = quantidade + ?, data_transacao = ? WHERE id_usuario = ? AND ticker = ?",
            "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, preço_unitario, tipo, data_transacao, transacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ], 

            [
            
            (quantidade, dataTransacao, session['id'], ticker),
            (session['id'], ticker, quantidade, valor, "COMPRA", dataTransacao, tipo),

        ])

    if code == 2:
        comandoSQL(
            [
                'INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, transacao ,preço_unitario, tipo, data_transacao) SELECT ?, ?, ?, ? (SELECT preco_medio FROM carteira_usuario WHERE id_usuario = ? AND ticker = ?), ?, ?',
                'DELETE FROM carteira_usuario WHERE id_usuario = ? AND ticker = ?',

            ],
            [
                (session['id'], ticker, quantidade, tipo, session['id'], ticker, "VENDA COMPLETA", dataTransacao),
                (session['id'], ticker),
            ]
        )

    if code == 3:
        comandoSQL(
            [
                "INSERT INTO carteira_usuario (id_usuario, ticker, nome, quantidade, data_transacao, tipo) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT (id_usuario, ticker) DO NOTHING",
                "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, preço_unitario, tipo, data_transacao, transacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                "INSERT INTO carteira_consolidada (id_usuario, valor, lucro_prejuizo, variacao) VALUES (?, ?, ? ,?) ON CONFLICT (id_usuario) DO NOTHING",
            ],
            [
                (session['id'], ticker, nome, quantidade, dataTransacao, tipo),
                (session['id'], ticker, quantidade, valor, "COMPRA", dataTransacao, tipo),
                (session['id'], (quantidade * valor), 0, '0'),
            ]
        )

    if code == 4:
        comandoSQL(  
            [
            "UPDATE carteira_usuario SET quantidade = quantidade - ?, data_transacao = ? WHERE id_usuario = ? AND ticker = ?",
            "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade,preço_unitario, tipo, data_transacao, transacao) VALUES (?, ?, ?, ?, ?, ?)",

            ], 
            [
            
            (quantidade, dataTransacao, session['id'], ticker,),
            (session['id'], ticker, quantidade, valor ,"VENDA", dataTransacao, tipo),

        ])

    if code == 5: consolidWallet()
    consolidWallet([], (), tipo)

def getVariacao():
    retorno = {}
    variacoes = comandoSQL(['SELECT * FROM carteira_variacao WHERE id_usuario = ?'], [(session['id'],)])[0]
    for index, variacao in  enumerate(variacoes, 1):
        retorno[index] = variacao
    return retorno