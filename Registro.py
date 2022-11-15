import sqlite3
from GetData import sqlString

def criaDB():
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (user TEXT UNIQUE, password TEXT , email TEXT UNIQUE, cpf TEXT UNIQUE)")
    con.close()
    
def registrar(nome = None ,senha = None ,email = None, cpf = None):
    email = str(email).lower()
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    
    cur.execute("INSERT INTO usuarios VALUES(?,?,?,?)", (nome,senha,email,cpf,))
    con.commit()
    con.close()

def logar(email= '', senha = ''):
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()

    cur.execute("SELECT email FROM usuarios")
    for email_sql in cur.fetchall():
        email_sql = sqlString(email_sql)
        if email_sql == '':
            con.execute("DELETE FROM usuarios WHERE email = ?", (email_sql,))
            con.commit()

        if email_sql == email:
            cur.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
            for password_sql in cur.fetchall():
                password_sql = sqlString(password_sql)
                if password_sql == senha:
                    return True
        else:
            return False

def retornDB(email = '', senha = ''):
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()

    cur.execute("SELECT email FROM usuarios")
    for email_sql in cur.fetchall():
        email_sql = sqlString(email_sql)
        if email_sql == '':
            con.execute("DELETE FROM usuarios WHERE email = ?", (email_sql,))
            con.commit()

        if email_sql == email:
            cur.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
            for password_sql in cur.fetchall():
                password_sql = sqlString(password_sql)
                if password_sql == senha:
                    cur.execute("SELECT user FROM usuarios WHERE email = ?", (email,))
                    user = sqlString(cur.fetchall()[0])
                    return user
