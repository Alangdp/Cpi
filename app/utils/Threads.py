from threading import Thread
from app.utils.Getdata import dataColect, Filter
from app.utils.extras import comandoSQL
from app.utils.carteira import comandoSQL as comandoSqlVarios
import sqlite3, time
import fundamentus
# Prototipo de uso de threads para auxilar na velocidade do refresh.


def criaDB():
    con = sqlite3.connect("Stocks.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Acoes (ticker text, name text, value text, dy_porcent text, dy_value text, tag_along text, roe text, margin text, dy6 text, img text, dpa text, filtered text )")
    con.close()

def threads(n):
    db = fundamentus.get_resultado()
    fragmentos = [db[i::n] for i in range(n)]
    return fragmentos

def getDatas(tickers, thread_name):
    inicioTempo = time.time()
    stock_info = []
    cont = 0
    total = len(tickers.index)
    for ticker in tickers.index:
        cont += 1
        print(ticker, thread_name, cont, (cont - total))
        stock_info.append(dataColect(ticker))
    setBancoDados(stock_info, inicioTempo)
    
def setBancoDados(lista,tempo):
    for x in lista:
        if x == None: continue
        comandoSqlVarios("INSERT INTO Acoes(ticker, name, value, dy_porcent, dy_value, tag_along, roe, margin, dy6, img, dpa, filtered) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) \
            ON CONFLICT(ticker) DO UPDATE SET \
                name = excluded.name, \
                value = excluded.value, \
                dy_porcent = excluded.dy_porcent, \
                dy_value = excluded.dy_value, \
                tag_along = excluded.tag_along, \
                roe = excluded.roe, \
                margin = excluded.margin, \
                dy6 = excluded.dy6, \
                img = excluded.img, \
                dpa = excluded.dpa, \
                filtered = excluded.filtered;", 
            (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img'],x['dpa'],'False', x['ticker']) )

    fimTempo = time.time()
    print(f"TEMPO DE EXECUÇÃO: {fimTempo - tempo}")

def activeThreads(fragmentos):
    cont = 0
    for x in fragmentos:
        Thread(target=getDatas, args=(fragmentos[cont], f'Thread-{cont + 1}')).start()
        cont += 1

def atualizaDB():
    criaDB()
    fragmentos = threads(70)
    activeThreads(fragmentos)
    Filter()
