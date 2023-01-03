import sqlite3
import fundamentus

def comandoSQL(comando, argumentos):
    con = sqlite3.connect("Stocks.db")
    cur = con.cursor()
    cur.execute(comando, argumentos)
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

def usuariosRegistrados():
    con = sqlite3.connect('Usuarios.db')
    cur = con.cursor()
    dados = []
    cur.execute("SELECT * FROM usuarios")
    for x in cur:
        dados.append({
            'user': x[0],
            'password': x[1],
            'email': x[2],
            'cpf': x[3],
        })
    return dados