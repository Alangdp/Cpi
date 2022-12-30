from threading import Thread
from GetData import *
from Registro import comandoSQL
import sqlite3
import fundamentus
# Prototipo de uso de threads para auxilar na velocidade do refresh.

def comandoSQL(comando, argumentos):
    con = sqlite3.connect("teste.db")
    cur = con.cursor()
    cur.execute(comando, argumentos)
    print(cur.description)
    if cur.description:
        retorno = cur.fetchall()
        con.close()
        if retorno == []:
            retorno = [0]
        return retorno
    else:
        con.commit()
        con.close()

def threads(n):
    db = fundamentus.get_resultado()
    fragmentos = [db[i::n] for i in range(n)]
    return fragmentos

def getDatas(tickers, thread_name):
    stock_info = []
    for ticker in tickers.index:
        print(ticker, thread_name)
        stock_info.append(coletaDados(ticker))
    setBancoDados(stock_info)
    
def setBancoDados(lista):
    for x in lista:
        comandoSQL("INSERT INTO teste VALUES(?,?,?,?,?,?,?,?,?,?,?)", (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img'],x['dpa']   ))

def activeThreads(fragmentos):
    cont = 0
    for x in fragmentos:
        Thread(target=getDatas, args=(fragmentos[cont], f'Thread-{cont + 1}')).start()
        cont += 1

fragmentos = threads(30)
activeThreads(fragmentos)




