from threading import Thread
from GetData import coletaDados, filtraMelhores
from extras import comandoSQL
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
        stock_info.append(coletaDados(ticker))
    setBancoDados(stock_info, inicioTempo)
    
def setBancoDados(lista,tempo):
    for x in lista:
        if x == None:
            continue
        comandoSQL("INSERT INTO Acoes VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img'],x['dpa'],'False' ,))
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
    filtraMelhores()


atualizaDB()


