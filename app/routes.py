from app import app
from flask import render_template
import GetData
petr4 = GetData.BasicData('petr4')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', petr4_name = petr4.Datas()['name'], petr4_dy = petr4.Datas()['dy_porcent'])