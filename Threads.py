from threading import Thread
from GetData import *
import sqlite3
import fundamentus

def threads(n):
    db = fundamentus.get_resultado()
    fragmentos = [db[i::n] for i in range(n)]
    return fragmentos

def getDatas(tickers, thread_name):
    tickers = list(tickers)

    stock_info = []
    for ticker in tickers:
        print(ticker, thread_name)
        stock_info.append(coletaDados(ticker))
    print(stock_info)



def activeThreads(fragmentos):
    cont = 0
    for x in fragmentos:
        Thread(target=getDatas, args=(fragmentos[cont], f'Thread-{cont + 1}')).start()
        cont += 1

fragmentos = threads(20)
activeThreads(fragmentos)

    

