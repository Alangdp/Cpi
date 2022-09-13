from app import app
from flask import render_template
import GetData
petr4 = GetData.BasicData('petr4')
bbas3 = GetData.BasicData('bbas3')
klbn3 = GetData.BasicData('klbn3')
taee11 = GetData.BasicData('taee11')
pssa3 = GetData.BasicData('pssa3')
rani3 = GetData.BasicData('rani3')
sanb3 = GetData.BasicData('sanb3')
itsa4 = GetData.BasicData('itsa4')
cple6 = GetData.BasicData('cple6')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            petr4_name = petr4.Datas()['name'], petr4_dy = petr4.Datas()['dy_porcent'], petr4_margin = petr4.Margin(),petr4_ranking = 1, petr4_mdi = 'TRUE',
                            petr4_value = petr4.Datas()['value'], petr4_highprice = petr4.Dy()['dy6'], petr4_img = 'static/petrlogo.png',
                           
                            bbas3_name = bbas3.Datas()['name'], bbas3_dy = bbas3.Datas()['dy_porcent'], bbas3_margin = bbas3.Margin(),bbas3_ranking = 2, bbas3_mdi = 'TRUE',
                            bbas3_value = bbas3.Datas()['value'], bbas3_highprice = bbas3.Dy()['dy6'], bbas3_img = 'static/bbaslogo.png',
                            
                            klbn3_name = klbn3.Datas()['name'], klbn3_dy = klbn3.Datas()['dy_porcent'], klbn3_margin = klbn3.Margin(),klbn3_ranking = 3, klbn3_mdi = 'TRUE',
                            klbn3_value = klbn3.Datas()['value'], klbn3_highprice = klbn3.Dy()['dy6'], klbn3_img = 'static/klbnlogo.png',
                            
                            taee11_name = taee11.Datas()['name'], taee11_dy = taee11.Datas()['dy_porcent'], taee11_margin = taee11.Margin(),taee11_ranking = 1, taee11_mdi = 'TRUE',
                            taee11_value = taee11.Datas()['value'], taee11_highprice = taee11.Dy()['dy6'], taee11_img = 'static/taee.png',
                            
                            pssa3_name = pssa3.Datas()['name'], pssa3_dy = pssa3.Datas()['dy_porcent'], pssa3_margin = pssa3.Margin(),pssa3_ranking = 1, pssa3_mdi = 'TRUE',
                            pssa3_value = pssa3.Datas()['value'], pssa3_highprice = pssa3.Dy()['dy6'], pssa3_img = 'static/pssa.png',
                            
                            rani3_name = rani3.Datas()['name'], rani3_dy = rani3.Datas()['dy_porcent'], rani3_margin = rani3.Margin(),rani3_ranking = 1, rani3_mdi = 'TRUE',
                            rani3_value = rani3.Datas()['value'], rani3_highprice = rani3.Dy()['dy6'], rani3_img = 'static/rani.png',
                            
                            sanb3_name = sanb3.Datas()['name'], sanb3_dy = sanb3.Datas()['dy_porcent'], sanb3_margin = sanb3.Margin(),sanb3_ranking = 1, sanb3_mdi = 'TRUE',
                            sanb3_value = sanb3.Datas()['value'], sanb3_highprice = sanb3.Dy()['dy6'], sanb3_img = 'static/sanb.png',
                          
                            itsa4_name = itsa4.Datas()['name'], itsa4_dy = itsa4.Datas()['dy_porcent'], itsa4_margin = itsa4.Margin(),itsa4_ranking = 1, itsa4_mdi = 'TRUE',
                            itsa4_value = itsa4.Datas()['value'], itsa4_highprice = itsa4.Dy()['dy6'], itsa4_img = 'static/itsa.png',
                            
                            cple6_name = cple6.Datas()['name'], cple6_dy = cple6.Datas()['dy_porcent'], cple6_margin = cple6.Margin(),cple6_ranking = 1, cple6_mdi = 'TRUE',
                            cple6_value = cple6.Datas()['value'], cple6_highprice = cple6.Dy()['dy6'], cple6_img = 'static/cple.png'
                           )