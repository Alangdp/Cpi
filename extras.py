import sqlite3
import fundamentus

def comandoSQL(comando, argumentos):
    con = sqlite3.connect("Stocks.db")
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

def trataErro(var):
    userName = []
    userId = []

    lista = var.split(',')
    for char in lista[0]:
        if char == '[' or char == ']' or char == "'" or char == '"'or char == '{'or char == '}':
            continue
        else:
            userName.append(char)
    userName = ''.join(userName).replace("name:", "")

    for char in lista[1]:
        if char.isnumeric():
            userId.append(char)
        else:
            continue
    userId = ''.join(userId)
    return userName, userId

def isTicker(ticker):
    ticker = (ticker).upper()
    acoes = fundamentus.get_resultado()
    for tick in acoes.index:
        if tick == ticker: return "True"
        else: continue
    return "False"
