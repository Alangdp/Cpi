import sqlite3
from GetData import sqlString

def criaDB():
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (user TEXT , password TEXT , email TEXT UNIQUE, cpf TEXT UNIQUE)")
    con.close()
    
def registrar(nome = None ,senha = None ,email = None, cpf = None):
    email = str(email).lower()
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios VALUES(?,?,?,?)", (nome,senha,email,cpf,))
    con.commit()
    cur.close()

def logar(email= '', senha = ''):
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()

    cur.execute("SELECT email FROM usuarios")
    for email_sql in cur.fetchall():
        email_sql = sqlString(email_sql)
        if email_sql == '':
            con.execute("DELETE FROM usuarios WHERE email = ?", (email_sql,))
            con.commit()
            cur.close()

        if email_sql == email:
            cur.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
            for password_sql in cur.fetchall():
                password_sql = sqlString(password_sql)
                if password_sql == senha:
                    return True
    con.close()

def retornDB(email = '', senha = ''):
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()


    cur.execute("SELECT email FROM usuarios")
    for email_sql in cur.fetchall():
        email_sql = sqlString(email_sql)
        if email_sql == '' or email_sql == None:
            print(email_sql)
            con.execute("DELETE FROM usuarios WHERE email = ?", (email_sql,))
            con.commit()
    con.close()
        
def fecharDB():
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    con.close()

def validaPost(usuario = '', email = '',senha = '' , cpf = ''):
    if usuario == '' or email == '' or senha == '' or cpf == '':
        return false
    else:
        return True
