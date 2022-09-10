from app import app
from flask import render_template
import GetData
petr4 = GetData.BasicData('petr4')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', petr4_name = petr4.Datas()['name'], petr4_dy = petr4.Datas()['dy_porcent'], petr4_margin = petr4.Margin(),petr4_ranking = 1, petr4_mdi = 'TRUE',
                           petr4_value = petr4.Datas()['value'], petr4_highprice = petr4.Dy()['dy6'])