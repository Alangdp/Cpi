import sqlite3, datetime, fundamentus, statistics
from flask import session
from .extras import isTicker as validaTicker

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
        data_transacao DATE NOT NULL
        );
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_usuario (
        id_usuario INTEGER NOT NULL,
        ticker VARCHAR(10) NOT NULL,
        nome VARCHAR(70) NOT NULL,
        quantidade DECIMAL(10, 0) NOT NULL,
        data_transacao DATE NOT NULL,
        preco_medio  DECIMAL(10,2),
        PRIMARY KEY (id_usuario, ticker)
        );
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS carteira_variacao (
        data DATE NOT NULL PRIMARY KEY,
        id_usuario INTEGER NOT NULL,
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

def consolidWallet(comands = [], arguments = []):
    dataAcao = datetime.date.today().strftime('%Y-%m-%d')
    comandos = []
    argumentos = []
    acoes = {}
    
    
    transacoes = comandoSQL(
        [
            'SELECT * FROM carteira_transacoes WHERE id_usuario = ?'
        ],
        [
            (session['id'],),
        ]
    )
    
    
    
    for transacao in transacoes[0]:
        ticker = transacao[2]
        quantidade = transacao[3]
        preco = transacao[4]

        if not acoes.__contains__(ticker): 
            cotacaoAtual = float(fundamentus.get_papel(ticker)['Cotacao'].iloc[0])
            acoes[ticker] = {'quantidade': 0, 'patrimonio': 0, 'valorAcao': cotacaoAtual}
        
        if transacao[5] == 'VENDA' or transacao[5] == 'VENDA COMPLETA': 
            quantidade = quantidade * -1

        acoes[ticker]['quantidade'] += quantidade
        acoes[ticker]['patrimonio'] += (preco * quantidade)

        try:
            acoes[ticker]['precoMedio'] = acoes[ticker]['patrimonio'] / acoes[ticker]['quantidade']
        except ZeroDivisionError:
            acoes[ticker]['precoMedio'] = 0

        precoMedio = float(f"{acoes[ticker]['precoMedio']:.2f}")

        if cotacaoAtual > precoMedio:
            acoes[ticker]['lucro_preju'] = f"{(cotacaoAtual - precoMedio) * int(acoes[ticker]['quantidade']):.2f}" 
        else:
            acoes[ticker]['lucro_preju'] = f"{(precoMedio - cotacaoAtual) * int(acoes[ticker]['quantidade']):.2f}"
        
        try:
            acoes[ticker]['variacao'] = f'{(cotacaoAtual - precoMedio) / precoMedio * 100:.2f}%'
        except ZeroDivisionError:
            acoes[ticker]['variacao'] = '0%'

    for ticker in acoes:
        comandos.append("UPDATE carteira_usuario SET preco_medio = ? WHERE id_usuario = ? AND ticker = ?")
        argumentos.append((acoes[ticker]['precoMedio'], session['id'], ticker,))

    valorTotal = 0
    lucroTotal = 0
    variacaoTotal = 0

    for ticker in acoes:
        variacaoTotal += float(acoes[ticker]['variacao'].replace('%', ''))
        lucroTotal += float(acoes[ticker]['lucro_preju'])
        valorTotal += float(acoes[ticker]['valorAcao'] * acoes[ticker]['quantidade'])

    '''
            data DATE NOT NULL PRIMARY KEY,
        id_usuario INTEGER NOT NULL,
        variacao VARCHAR(10),
        valorCarteira DECIMAL(10,2)
    '''

    comandoSQL(["UPDATE carteira_consolidada SET valor = ? ,lucro_prejuizo = ? , variacao = ? WHERE id_usuario = ?",
                "INSERT OR REPLACE INTO carteira_variacao (data, id_usuario, variacao, valorCarteira) VALUES (?, ?, ?, ?)",
            ],
               [(valorTotal, lucroTotal,variacaoTotal, session['id'],),
                (dataAcao, session['id'], variacaoTotal, valorTotal,),
            ]) 

    if len(comands) > 0:
        comandos.extend(comands)
        argumentos.extend(arguments)

    dados = comandoSQL(comandos, argumentos)
    return dados

def updateWallet(ticker = '', quantidade = 0, valor = 0, code = 1):
    dataTransacao = datetime.date.today().strftime('%Y-%m-%d')
    if quantidade <= 0: return
    if code < 3 and code > 0: 
        if not validaTicker(ticker): return

    stockInfo = fundamentus.get_papel(ticker)
    nome = stockInfo['Empresa'].iloc[0]

    if code == 1:
        comandoSQL(  
            [
            "UPDATE carteira_usuario SET quantidade = quantidade + ?, data_transacao = ? WHERE id_usuario = ? AND ticker = ?",
            "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, preço_unitario, tipo, data_transacao) VALUES (?, ?, ?, ?, ?, ?)",

            ], 

            [
            
            (quantidade, dataTransacao, session['id'], ticker,),
            (session['id'], ticker, quantidade, valor, "COMPRA", dataTransacao,),

        ])
        consolidWallet()

    if code == 2:
        comandoSQL(
            [
                'INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, preço_unitario, tipo, data_transacao) SELECT ?, ?, ?, (SELECT preco_medio FROM carteira_usuario WHERE id_usuario = ? AND ticker = ?), ?, ?',
                'DELETE FROM carteira_usuario WHERE id_usuario = ? AND ticker = ?',

            ],
            [
                (session['id'], ticker, quantidade, session['id'], ticker, "VENDA COMPLETA", dataTransacao),
                (session['id'], ticker),
            ]
        )
        consolidWallet()

    if code == 3:
        comandoSQL(
            [
                "INSERT INTO carteira_usuario (id_usuario, ticker, nome, quantidade, data_transacao) VALUES (?, ?, ?, ?, ?) ON CONFLICT (id_usuario, ticker) DO NOTHING",
                "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade, preço_unitario, tipo, data_transacao) VALUES (?, ?, ?, ?, ?, ?)",
                "INSERT INTO carteira_consolidada (id_usuario, valor, lucro_prejuizo, variacao) VALUES (?, ?, ? ,?) ON CONFLICT (id_usuario) DO NOTHING",
            ],
            [
                (session['id'], ticker, nome, quantidade, dataTransacao,),
                (session['id'], ticker, quantidade, valor, "COMPRA", dataTransacao,),
                (session['id'], (quantidade * valor), 0, '0'),
            ]
        )
        consolidWallet()

    if code == 4:
        comandoSQL(  
            [
            "UPDATE carteira_usuario SET quantidade = quantidade - ?, data_transacao = ? WHERE id_usuario = ? AND ticker = ?",
            "INSERT INTO carteira_transacoes (id_usuario, ticker, quantidade,preço_unitario, tipo, data_transacao) VALUES (?, ?, ?, ?, ?, ?)",

            ], 
            [
            
            (quantidade, dataTransacao, session['id'], ticker,),
            (session['id'], ticker, quantidade, valor ,"VENDA", dataTransacao,),

        ])
        consolidWallet()

    if code == 5: consolidWallet()