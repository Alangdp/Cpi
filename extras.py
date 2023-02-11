import sqlite3, fundamentus, re, socket
from flask import request, redirect, session

def genAlert(typeA, message):
    session[typeA] = message

def validaSenha(senha = ''):
    if not re.match(r' /^(?=.*\d)(?=.*[!@#$%^&*(){}])(?=.*[a-z])(?=.*[A-Z]).{8,12}$/', senha): return False
    print('senha passou')
    return True

def validaEmail(email = ''):
    if not re.match(r"^\S+@\S+\.\S+$", email): return False
    print('email passou')
    return True

# def validaMX(email = ''):
#     dominio = email.split("@")[-1]
#     try:
#         MX = socket.getaddrinfo(dominio, None, socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
#         if not MX: return False
#         return True
#     except socket.gaierror:
#         return False

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

def validaCSR(token = ''):

    if not 'csrfToken' in session: return False
    if not token == session['csrfToken']: return False
    print(123454566)
    return True
