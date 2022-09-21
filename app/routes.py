from app import app
from flask import render_template
from flask import request
import teste2
import GetData

Acoes = teste2.getLocalData()
quantidade = len(Acoes)

@app.route('/')
@app.route('/index')
@app.route('/ranking')
def ranking():
    return render_template('ranking.html',stock = Acoes, qt = quantidade)
    
@app.route('/registrar')
def regristrar():
    return render_template('register.html')

@app.route('/detalhes', methods=['GET','POST'])
def detalhes():
    try:
        ticker = request.args.get('ticker')
        ticker.upper()
    except:
        if ticker == None:
            pass
    stock = GetData.BasicData(ticker)
    print(stock)
    return stock


# @app.route('/test')
# def test():
#     return render_template('teste.html',stock = Acoes, qt = quantidade)
                        