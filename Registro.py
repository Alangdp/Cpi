import sqlite3
from flask import flash
from GetData import sqlString
from hashlib import sha256
from flask import session
from extras import *

def atualizarSenha(novaSenha, senhaAtual, idd):
    if not validaSenha(senhaAtual): return
    if not validaSenha(novaSenha): return

    senhaAtual = sha256(senhaAtual.encode()).hexdigest()
    novaSenha = sha256(novaSenha.encode()).hexdigest()

    if senhaAtual != session['user'][0][1]:
        flash('Senha atual inválida', 'ErrorUserPassword')
        return
    else:
        comandoSQL('UPDATE usuarios SET password = ? WHERE id = ?', (novaSenha, idd, ))
        flash('Senha Alterada', 'SucessUserPassword')
        return
    

def atualizarEmail(novoEmail, EmailAtual, idd):
    if not validaEmail(novoEmail): return
    if not validaEmail(EmailAtual): return

    EmailAtual = EmailAtual.lower()
    novoEmail = novoEmail.lower()

    if EmailAtual != session['user'][0][2]:
        flash('Email atual inválido', 'ErrorUserEmail')
        return
    else:  
        comandoSQL('UPDATE usuarios SET email = ? WHERE id = ?', (novoEmail, idd, ))
        flash('Email alterado', 'SucessUserEmail')
        return

def deslogar():
    session['logged'] = False

def comandoSQL(comando, argumentos):
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute(comando, argumentos)
    if cur.description:
        retorno = cur.fetchall()
        con.close()
        return retorno
    else:
        con.commit()
        con.close()

def criaDB():
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (user TEXT , password TEXT , email TEXT UNIQUE, cpf TEXT UNIQUE, id INTEGER PRIMARY KEY AUTOINCREMENT)")
    
    con.close()
    
criaDB()

def registrarDB(nome = None ,senha = None ,email = None, cpf = None):
    email = str(email).lower()
    # if not validaSenha(senha): return
    # if not validaEmail(email): return
    senha = sha256(senha.encode()).hexdigest()

    try:
        comandoSQL("INSERT INTO usuarios (user,password,email,cpf) VALUES(?,?,?,?)", (nome,senha,email,cpf,))
        return True
    except:
        gerarAviso('Cpf Já cadastrado')
        return False

    # REFATORADO

    '''
    email = str(email).lower()
    senha = sha256(senha.encode()).hexdigest()
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios VALUES(?,?,?,?)", (nome,senha,email,cpf,))
    con.commit()
    cur.close()
    '''

def logar(email= '', senha = ''):
    email = email.lower()

    # if not validaSenha(senha): return False
    # if not validaEmail(email): return False

    senha = sha256(senha.encode()).hexdigest()
    senha_sql = comandoSQL("SELECT password, id FROM usuarios WHERE email = ?", (email.lower(),))

    if senha == sqlString(senha_sql[0][0]): 
        session['id'] = senha_sql[0][1]
        session['logged'] = True
        session['user'] = retornDB(email, senha)
        return True
    else: 
        gerarAviso('Senha ou email incorretos')
        return False

    # REFATORADO

    # def logar(email= '', senha = ''):
    # con = sqlite3.connect("Usuarios.db")
    # cur = con.cursor()
    # senha = sha256(senha.encode()).hexdigest()
    # cur.execute("SELECT email FROM usuarios")
    # for email_sql in cur.fetchall():
    #     email_sql = sqlString(email_sql)
    #     if email_sql == '':
    #         con.execute("DELETE FROM usuarios WHERE email = ?", (email_sql,))
    #         con.commit()
    #         cur.close()

    #     if email_sql == email:
    #         cur.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
    #         for password_sql in cur.fetchall():
    #             password_sql = sqlString(password_sql)
    #             if password_sql == senha:
    #                 con.close()
    #                 return True
    # con.close()
    
def retornDB(email = '', senha = ''):
    try:
        user = comandoSQL("SELECT * FROM usuarios WHERE id = ?", (session['id'],))   
        return user
    except:
        return None

    # REFATORADO
    
    '''
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM usuarios")
    senha = sha256(senha.encode()).hexdigest()
    try:
        for emailSQL in cur:
            emailSQL = sqlString(emailSQL)
            if email == emailSQL:
                cur.execute("SELECT password FROM usuarios")
                for senhaSQL in cur:
                    senhaSQL = sqlString(senhaSQL)
                    if senha == senhaSQL:
                        cur.execute("SELECT user FROM usuarios WHERE email =?", (email, ))
                        for user in cur:
                            user = sqlString(user)
                            con.close()
                            return user
    except:
        con.close()
    '''

def validaPostR(usuario = '', email = '',senha = '' , cpf = ''):
    if usuario == '' or email == '' or senha == '' or cpf == '':
        return False
    else:
        return True