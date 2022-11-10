import sqlite3

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
    