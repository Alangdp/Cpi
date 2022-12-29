import sqlite3
from GetData import sqlString
from hashlib import sha256

def comandoSQL(comando, argumentos):
    con = sqlite3.connect("Usuarios.db")
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

def criaDB():
    con = sqlite3.connect("Usuarios.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (user TEXT , password TEXT , email TEXT UNIQUE, cpf TEXT UNIQUE)")
    con.close()
    
criaDB()

def registrar(nome = None ,senha = None ,email = None, cpf = None):
    email = str(email).lower()
    senha = sha256(senha.encode()).hexdigest()
    comandoSQL("INSERT INTO usuarios VALUES(?,?,?,?)", (nome,senha,email,cpf,))

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
    senha = sha256(senha.encode()).hexdigest()
    senha_sql = comandoSQL("SELECT password FROM usuarios WHERE email = ?", (email,))
    if senha == sqlString(senha_sql[0]): 
        return True
    else: 
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
    email = str(email).lower()
    senha = sha256(senha.encode()).hexdigest()
    try:
        user = comandoSQL("SELECT user FROM usuarios WHERE password = ? AND email = ?", (senha, email,))   
        user = sqlString(user[0])
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

def validaPostL(email = '', senha = '' ):
    if email == '' or senha == '':
        return False
    else:
        return True
