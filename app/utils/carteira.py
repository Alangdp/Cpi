import sqlite3, datetime, fundamentus, statistics, requests, requests_cache
from flask import session
from app.utils.extras import isTicker as validaTicker
from app.utils.Getdata import sqlString
import pandas as pd, json, requests


def changeSelicIbov(All = False):
    dataAtual = datetime.date.today().strftime('%Y/%m/%d')
    ibov = getYahooAPI("IBOV11")['Variacao']
    selic = json.loads(requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos").content)[0]['valor']

    con = sqlite3.connect(path)
    cur = con.cursor()
    IDS = []

    if All == True: IDS = list(cur.execute("SELECT id_usuario FROM carteira_consolidada").fetchall()[0])
    print(IDS)
    # if IDS == []:
    #     return
    for Id in [session['id']]:
        dadosSelic = cur.execute("SELECT id_usuario, data FROM carteira_variacao WHERE id_usuario = ? AND data = ? AND tipo = 'SELIC' ", (1, dataAtual))
        dadosIbov = cur.execute("SELECT id_usuario, data FROM carteira_variacao WHERE id_usuario = ? AND data = ? AND tipo = 'IBOV' ", (1, dataAtual))

        if dadosSelic.fetchone() != None or dadosIbov.fetchone() != None: 
            cur.execute("UPDATE carteira_variacao SET variacao = ? WHERE data = ? AND id_usuario = ? AND tipo = 'SELIC' ", (selic, dataAtual, Id))
            cur.execute("UPDATE carteira_variacao SET variacao = ? WHERE data = ? AND id_usuario = ? AND tipo = 'IBOV' ", (ibov, dataAtual, Id))
        else:
            cur.execute("INSERT INTO carteira_variacao (data, id_usuario, variacao, valorCarteira, tipo) VALUES (?, ?, ?, ?, ?);", (dataAtual, Id, selic, 0, "SELIC"))
            cur.execute("INSERT INTO carteira_variacao (data, id_usuario, variacao, valorCarteira, tipo) VALUES (?, ?, ?, ?, ?);", (dataAtual, Id, ibov, 0, "IBOV"))

        if All == False:
            selicSoma = cur.execute("SELECT id_usuario, tipo, SUM(variacao) as total_variacao FROM carteira_variacao WHERE id_usuario = ? AND tipo = 'SELIC' GROUP BY id_usuario, tipo", (Id,)).fetchone()
            ibovSoma = cur.execute("SELECT id_usuario, tipo, SUM(variacao) as total_variacao FROM carteira_variacao WHERE id_usuario = ? AND tipo = 'IBOV' GROUP BY id_usuario, tipo", (Id,)).fetchone() 
            
            retorno = {}

            retorno['SELIC'] = {'Valor': selicSoma[2]}
            retorno['IVOB'] = {'Valor': ibovSoma[2]}

            con.commit()
            con.close()

            return retorno
        
    con.commit()
    con.close()

    return


def existDate(ids = [], dataAtual = '', info = {}, selic = 0, ibov = 0):
    ignorar = ['valorTotal', 'lucroTotal', 'variacaoTotal']
    comandos = []
    argumentos = []

    con = sqlite3.connect(path)
    cur = con.cursor()
    uniqueIds = list(set(ids))

    for Id in uniqueIds:
        dados = cur.execute("SELECT id_usuario, data FROM carteira_variacao WHERE id_usuario = ? AND data = ? AND tipo = 'variacao' ", (Id, dataAtual))
        print(dados.fetchone())
        if dados.fetchone() != None:
            comandos.append("UPDATE carteira_variacao SET variacao = ?, valorCarteira = ? WHERE id_usuario = ? AND data = ? AND tipo = variacao")
            argumentos.append((info[Id]['variacaoTotal'], info[Id]['valorTotal'], Id, dataAtual))
        else:
            comandos.append("INSERT INTO carteira_variacao (data, id_usuario, variacao, valorCarteira, tipo) VALUES (?, ?, ?, ?, ?);")
            argumentos.append((dataAtual, Id, info[Id]['variacaoTotal'], info[Id]['valorTotal'], "variacao"))
    con.close()
    print(comandos, argumentos)
    return {'comandos': comandos, 'argumentos': argumentos}

def getYahooAPI(ticker = ''):
    if not ticker: return None
    hdr = {
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
        'Accept-Encoding': 'gzip, deflate',
    }
        
    querystring = {"q":f"{ticker}","region":"BR"}
    response = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}.SA', headers=hdr, params=querystring)
    dados = json.loads(response.content )

    filtrado = {
        "Nome": dados['quoteResponse']['result'][0]['shortName'],
        "valorAtual": dados['quoteResponse']['result'][0]['regularMarketPrice'],
        "Variacao": dados['quoteResponse']['result'][0]['regularMarketChangePercent']
    }
    return  filtrado

# API COM VALORES DESATUALIZADOS
# def fundamentaRaw(ticker=''):
#     url = 'http://fundamentus.com.br/detalhes.php?papel={}'.format(ticker)
#     hdr = {
#         'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#         'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
#         'Accept-Encoding': 'gzip, deflate',
#     }

#     with requests_cache.enabled():
#         content = requests.get(url, headers=hdr)
    
#     tables = pd.read_html(content.text, decimal=',', thousands='.')
#     df = tables[0]

#     print(df)
#     return df

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
        id_usuario INTEGER NOT NULL,
        variacao VARCHAR(10),
        valorCarteira DECIMAL(10,2),
        tipo VARCHAR(10)
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
    porcent = {'valorTotal': 0, 'Acao': {'valor': 0, 'quantidade': 0, 'porcentagem': 0, 'tickers' : {}}, 'Fii': {'valor': 0, 'quantidade': 0, 'porcentagem': 0, 'tickers' : {}} }

    for ativo in carteira:
        ticker = ativo[1]
        quantidade = ativo[3]
        tipo = ativo[6]

        if tipo == 'Fii':
            cotacaoAtual = getYahooAPI(ticker)['valorAtual']
            porcent['Fii']['valor'] += round((quantidade * cotacaoAtual), 2)
            porcent['Fii']['quantidade'] += quantidade
            
        if tipo == 'Acao':
            cotacaoAtual = getYahooAPI(ticker)['valorAtual']
            porcent['Acao']['valor'] += round((quantidade * cotacaoAtual), 2)
            porcent['Acao']['quantidade'] += quantidade

        porcent['valorTotal'] += round((quantidade * cotacaoAtual), 2)

    for ativo in carteira:
        ticker = ativo[1]
        tipo = ativo[6]
        quantidade = ativo[3]

        if tipo == 'Fii':
            
            cotacaoAtual = getYahooAPI(ticker)['valorAtual']
            valorTotalAtivo = round(quantidade * cotacaoAtual, 2)
            porcent['Fii']['tickers'][ticker] = {'valor': valorTotalAtivo, 'porcentagem': round(valorTotalAtivo / porcent['Fii']['valor'] * 100, 2)}
            
        if tipo == 'Acao':
            cotacaoAtual = getYahooAPI(ticker)['valorAtual']
            valorTotalAtivo = round(quantidade * cotacaoAtual, 2)
            porcent['Acao']['tickers'][ticker] = {'valor': valorTotalAtivo, 'porcentagem': round(valorTotalAtivo / porcent['Acao']['valor'] * 100, 2)}
        
    for chave in porcent:
        if chave == 'valorTotal': continue
        try:
            porcent[chave]['porcentagem'] = round((porcent[chave]['valor'] / porcent['valorTotal']) * 100, 2)
        except ZeroDivisionError:
            porcent[chave]['porcentagem'] = 0

    return porcent

def consolidWallet(comands = [], arguments = [], All = False, selic = 0, ibov = 0 ):
    dataAcao = datetime.date.today().strftime('%Y/%m/%d')
    comandos = []
    argumentos = []
    acoes = {}
    LIDS = [] # IDS

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
                cotacaoAtual = getYahooAPI(ticker)['valorAtual']
                
            if tipo == 'Acao':
                cotacaoAtual = getYahooAPI(ticker)['valorAtual']
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

        acoes[Id][ticker]['lucro_preju'] = f"{(cotacaoAtual - precoMedio) * int(acoes[Id][ticker]['quantidade']):.2f}" 
        try:
            acoes[Id][ticker]['variacao'] = f'{(cotacaoAtual - precoMedio) / precoMedio * 100:.2f}%'
        except ZeroDivisionError:
            acoes[Id][ticker]['variacao'] = '0%'

        acoes[Id]['valorTotal'] = 0
        acoes[Id]['lucroTotal'] = 0
        acoes[Id]['variacaoTotal'] = 0

    LIDS = list(set(LIDS))
    for Id in LIDS:
        for ticker in acoes[Id]:
            if ticker == 'valorTotal' or ticker == 'lucroTotal' or ticker == 'variacaoTotal':
                continue
            comandos.append("UPDATE carteira_usuario SET preco_medio = ? WHERE id_usuario = ? AND ticker = ?")
            argumentos.append((acoes[Id][ticker]['precoMedio'], Id, ticker,))
            
        for ticker in acoes[Id]:
            if ticker == 'valorTotal' or ticker == 'lucroTotal' or ticker == 'variacaoTotal':
                continue

            acoes[Id]['variacaoTotal'] += float(acoes[Id][ticker]['variacao'].replace('%', ''))
            acoes[Id]['lucroTotal'] += float(acoes[Id][ticker]['lucro_preju'])
            acoes[Id]['valorTotal'] += float(acoes[Id][ticker]['valorAcao'] * acoes[Id][ticker]['quantidade'])

        for ticker in acoes[Id]:
            comandos.append("UPDATE carteira_consolidada SET valor = ? ,lucro_prejuizo = ? , variacao = ? WHERE id_usuario = ?")
            argumentos.append((acoes[Id]['valorTotal'], acoes[Id]['lucroTotal'], acoes[Id]['variacaoTotal'], Id,))

    dadosAtualizar = existDate(LIDS, dataAcao, acoes)
    comandos.extend(dadosAtualizar['comandos'])
    argumentos.extend(dadosAtualizar['argumentos'])

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
        df = getYahooAPI(ticker)
        nome = df['Nome']

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
                "INSERT INTO carteira_consolidada (id_usuario, valor, lucro_prejuizo, variacao) VALUES (?, ?, ?, ?) ON CONFLICT (id_usuario) DO NOTHING",
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
    variacoes = comandoSQL(['SELECT * FROM carteira_variacao WHERE id_usuario = ? ORDER BY tipo ASC'], [(session['id'],)])
    chave_anterior = None
    index = 0
    print(porcentWallet())
    for variacao in variacoes[0]:
        variacao = list(variacao)
        variacao[2] = round(float(variacao[2]), 2)
        if variacao[4] != chave_anterior:
            index = 0
        if variacao[4] not in retorno:
            retorno[variacao[4]] = {}
        
        retorno[variacao[4]][index] = variacao
        chave_anterior = variacao[4]
        index += 1
    return retorno