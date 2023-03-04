from bs4 import BeautifulSoup
from mechanize import Browser
from extras import comandoSQL
from lxml import etree
import datetime
import fundamentus, lxml, shutil, requests, json, datetime
# from selenium import webdriver

# Global Methods
        
def formate_Number(x, virgulas = 2):
    lt = []
    for y in str(x):
        if y == ',':
            lt.append('.')
            continue
        if y.isnumeric():
            lt.append(y)
        else: 
            pass
    formated = float(''.join(lt))
    return float(f'{formated:.{virgulas}f}')

def sqlString(valor):
    try:
        string = ''.join(valor)
        return string
    except:
        return valor

def highdy():
    total = [], info = []
    df = fundamentus.get_resultado()
    for index in df.index:  
        try:
            print(index, len(info))
            print(index, 'etapa 1', len(info))
            stock = BasicData(index)
            print(df['dy'][index], df['mrgliq'][index])
            if (( not (df['dy'][index]  > 0.5 or df['dy'][index] < 0.06)) and df['mrgliq'][index] >= 0):
                if stock.Margin() > 100:
                        continue
                else:
                    if stock.Datas()['p_vp'] <= 2.5 and stock.Datas()['pl'] <= 15:
                        if stock.Datas()['payout'] <= 10:
                            continue
                        else:
                            info.append(index)
                            print(index, 'etapa2', len(info))              
        except:
            continue
    selecionados(info)

def filtraMelhores():
    selecionadosValido = [] 
    df = fundamentus.get_resultado()
    for ticker in df.index:
        try:
            stock = BasicData(ticker)
            data = stock.Datas()
            if not (df['dy'][ticker] > 0.5 or df['dy'][ticker] < 0.05): continue
            elif df['mrgliq'][ticker] <= 0: continue
            elif stock.Margin() > 100: continue
            elif data['p_vp'] > 2.5 and data['pl'] > 15: continue
            elif data['payout'] <= 10: continue
            else: selecionadosValido.append(ticker)
        except:
            continue
    selecionados(selecionadosValido)
        
def selecionados(lista):
    comandoSQL("UPDATE Acoes set filtered = ?", ("False",))
    for ticker in lista:
        comandoSQL("UPDATE Acoes set filtered = True WHERE ticker = ?", (ticker, ))

def selecionadosCard():
    lista = []
    retornavel = []
    tickers = comandoSQL("SELECT ticker FROM Acoes WHERE filtered = ?", ("1",))
    for tickerSet in tickers:
        tickerString = sqlString(tickerSet)
        infos = comandoSQL("SELECT * FROM Acoes WHERE ticker = (?) ORDER BY CAST(margin as REAL)", (tickerString,))
        info = ([info for info in infos])
        lista.append(info)
    for info in lista:
        retornavel.append(info[0])
    return retornavel
        
def coletaDados(x):
    listaDeErros = []
    tic = x
    try:
        
        if '33' in tic or '5' in tic:
            pass
        stock = BasicData(tic)
        data = stock.Datas()
        dy = stock.Dy()

        # ERRO NO DB BLOCK LH CLASS

        info = {
            'ticker':stock.ticker,
            'name':data['name'],
            'value':data['value'],
            'dy_porcent':data['dy_porcent'],
            'dy_value':data['dy_value'],
            'tag_along':data['tag_along'],
            'roe':data['roe'],
            'margin':float(stock.Margin()),
            'dy6':dy['dy6'],
            'dpa':dy['dpa'],
            'img':stock.getImage(),
        }

        print(f'Retornado {tic}')
        return info
    except:
        listaDeErros.append(tic)
        pass
    

def sqUpdate(data):
    data = list(data)
    import sqlite3
    con = sqlite3.connect('TopStocks.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Acoes (ticker text, name text, value text, dy_porcent text, dy_value text, tag_along text, roe text, margin text, dy6 text, img text, dpa text)")
    for x in (data):
        if x == None:
            continue
        print(x)
        cur.execute("INSERT INTO Acoes VALUES(?,?,?,?,?,?,?,?,?,?,?)", (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img'],x['dpa']   ))
        con.commit()
        
    con.close()

def getLocalData():
    
    import sqlite3
    try:
        con = sqlite3.connect('TopStocks.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Acoes ORDER BY margin")
        tickers = []
        cur.execute("SELECT * FROM Acoes")
        for x in cur:
            tickers.append(x)
        con.close()
        return list(tickers)
    except:
        con = sqlite3.connect('TopStocksBU.db')
        cur = con.cursor()
        tickers = []
        cur.execute("SELECT * FROM Acoes")
        for x in cur:
            tickers.append(x)
        con.close()
        return list(tickers)

# Classe de coleta de dados

class BasicData():

    def __init__(self,ticker):
        if ticker == None:
            exit()
        else:
            self.ticker = ticker.upper()
            self.data = datetime.date.today()

        
    def Soup(self, args=None):
        try:
            b = Browser()
            b.set_handle_robots(False)
            b.addheaders = [('Referer', 'https://statusinvest.com.br'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
            b.open(f'{self.links()}')
            page = b.response().read()
            soup = BeautifulSoup(page, "lxml")
            return soup
        except:
            return 'ERRO SOUP'

    def requestsCaixa(self):
        ano = self.data.year
        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'https://statusinvest.com.br/acao/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        b.open(f'https://statusinvest.com.br/acao/getativos?code={self.ticker}&type=0&futureData=false&range.min=2017&range.max={ano}')
        page = b.response().read()
        data = json.loads(page)
        return data

    def fluxoCaixa(self):
        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'https://statusinvest.com.br/acao/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        b.open(f'https://statusinvest.com.br/acao/getfluxocaixa?code={self.ticker}&type=0&futureData=true')
        page = b.response().read()
        data = json.loads(page)
        return data
        
    def SoupP(self, args=None):
        try:
            link = BasicData(self.ticker)
            url = (link.linksP())
            session = requests.Session()
            page = session.get(url)
            soup = BeautifulSoup(page.text, "lxml")
            return soup
        except:
            return 'ERRO SOUP'

    def links(self, args=None):
        try:
            self.ticker = self.ticker.upper()
            link = f'https://statusinvest.com.br/acoes/{self.ticker}'
            return str(link)
        except:
            return 'ERRO LINK'
    
    def linksP(self, args=None):
        try:
            self.ticker = self.ticker.upper()
            link = f'https://www.guiainvest.com.br/raiox/{self.ticker}.aspx'
            return str(link)
        except:
            return 'ERRO LINK'
        
    def buyBack(self, args=None):
        self.soup = self.Soup()
        try:
            infoBB = {}
            self.buyback = self.soup.find('div',class_='buyback card')
            self.buyback = self.buyback.find('div', class_='card-body')
            self.aproved = self.buyback.findAll('span',class_='d-block fw-700')[0].text
            self.active = self.buyback.find('span', class_='badge main-badge white-text darken-3 green').text
            self.type = self.buyback.findAll('span',class_='d-block fs-4 lh-4 fw-700')[0].text
            self.quantify = self.buyback.findAll('span', class_='d-block fs-4 lh-4 fw-700')[1].text
            self.init = self.buyback.findAll('span', class_='d-block fw-700')[1].text
            self.end = self.buyback.findAll('span', class_='d-block fw-700')[2].text
            
            infoBB['buybakck_type'] = self.type
            infoBB['buyback_quantify'] = self.quantify
            infoBB['buyback_active'] = self.active
            infoBB['buyback_aproved'] = self.aproved
            infoBB['buyback_init'] = self.init
            infoBB['buyback_end'] = self.end
            
            return infoBB
        except:
            return 'ERRO INFO DATA BUYBACK'
    
    def Datas(self, args=None):
        
        self.soup = self.Soup()
        self.soupP = self.SoupP()
        
        # Informações mais importantes, dados do html
        
        try:
            self.ri = self.soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow", "class": "waves-effect waves-light btn btn-small btn-secondary"})[0]["href"]
        except:
            self.ri = None
        
        try: 
            self.payout = formate_Number(self.soupP.find('span',attrs={'id': 'lbPayout1'}).text)
        except:
            self.payout = 0.001
            
        try:
            self.value_dblock_class = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})
        except: 
            return 'ERRO DB BLOCK LH CLASS '
        
        try:
            self.value_class = self.soup.findAll(attrs={'class':'value'})
        except:
            return 'ERRO VALUE CLASS'
        
        try:
            self.strong_class = self.soup.findAll('strong',attrs={'class':'value'})
        except:
            return 'ERRO STRONG CLASS'
        try:
            self.value_sub_class = self.soup.findAll('span' ,attrs={'class':'sub-value'})
        except:
            return 'ERRO VALUE CLASS'
        
        # Dados e tratamento se nescessário

        self.name = self.soup.find('small').text
        self.value = self.value_class[0].text
        self.value = float(formate_Number(self.value))
        self.dy_Value = self.value_sub_class[3].text
        self.div_liq = self.strong_class[91].text
        self.div_brt = self.strong_class[89].text
        self.dy_Porcent = self.value_class[3].text
        self.dy_Value = formate_Number(self.dy_Value)
        self.tagAlong = self.value_class[6].text
        self.p_vp = self.value_dblock_class[3].text
        self.p_vp = formate_Number(self.p_vp)
        self.roe = self.value_dblock_class[24].text   
        self.pl = self.value_dblock_class[1].text
        self.pl = formate_Number(self.pl)
        self.divLiq_ebitda = self.soup.findAll('div', class_='d-flex align-items-center justify-between pr-1 pr-xs-2')[15]
        
        
        # Checagens se vazio substituir
        
        if str(self.dy_Porcent) == '-':
            self.dy_Porcent = '0.01'
        else:
            self.dy_Porcent = formate_Number(self.dy_Porcent)
            
        if self.dy_Value == '-':
            self.dy_Value = 0
            
        if '-' in self.tagAlong:
            self.tagAlong = '0.00'
            
        # Montagem do dicionário
            
        try:
            info = {}
            info['ticker'] = self.ticker
            info['name'] = self.name
            info['value'] = self.value
            info['dy_value'] = self.dy_Value
            info['dy_porcent'] = self.dy_Porcent
            info['p_vp'] = self.p_vp
            info['roe'] = self.roe
            info['tag_along'] = self.tagAlong
            info['pl'] = self.pl
            info['payout'] = self.payout
            info['ri_page'] = self.ri
            info['div_liq'] = self.div_liq
            info['div_brt'] = self.div_brt
            info['divliq_ebitda'] = 0
            # info['buybakck_type'] = self.type
            # info['buyback_quantify'] = self.quantify
            # info['buyback_active'] = self.active
            # info['buyback_aproved'] = self.aproved
            # info['buyback_init'] = self.init
            # info['buyback_end'] = self.end
        except:
            return 'ERRO INFO DATAS'
        
        return info
        
    def fundamentalDatas(self):
        self.soup = self.Soup() 
        self.soupP = self.SoupP()
        
        # Informações mais importantes, dados do html
        
        try:
            self.strong_class = self.soup.findAll('strong', class_="value")
        except:
            return 'ERRO STRONG CLASS'
        
        # Coleta de informações e tratamento se nescessário
        
        self.segment = self.soupP.find(id="hlSubsetor").text
        self.listing = self.soupP.find(id="lbGovernanca").text
        self.market_value = int((formate_Number(self.soupP.find(id='lbValorMercado1').text))* 1000)
        self.ultimofechamento = self.soupP.find('span', attrs={'id': 'lbUltimoFechamento'}).text
        self.valorMercado = self.soupP.find('span', attrs = {'id': 'lbValorMercado1'}).text
        self.volume = self.soup.findAll('strong', attrs={'class':'m-md-0 mb-md-1 value mt-0 fs-3_5 lh-4'})[1].text
        self.acoesEmitidas = self.soup.find('div', attrs={'title' : 'Total de papéis disponíveis para negociação'}).find('strong', attrs={'class': 'value'}).text
        self.valor_12 = self.strong_class[4].text
        self.min_12 = self.strong_class[2].text
        self.max_12 = self.strong_class[1].text
        self.paper_volume = formate_Number(self.soupP.find('span', id="lbInformacaoAdicionalQuantidadeTotalAcao").text)*1000
        self.end_value = formate_Number(self.soupP.find('span', id="lbUltimoFechamento"))
        requestAtivos = self.requestsCaixa()
        caixa = requestAtivos['data']['grid'][4]['gridLineModel']['values'][0]
        self.caixa = f"{caixa:,.0f}"
        fluxoCaixa = self.fluxoCaixa()
        self.lucroLiquido = fluxoCaixa['data']['grid'][3]['gridLineModel']['values'][0]

        try:
            info = {}
            info['valor_12'] = self.valor_12
            info['min_12'] = self.min_12
            info['max_12'] = self.max_12
            info['segment'] = self.segment
            info['listing'] = self.listing
            info['ibov'] = 123
            info['volume'] = self.volume
            info['end'] = self.end_value
            info['paperM'] = self.paper_volume
            info['ultimoFechamento'] = self.ultimofechamento
            info['valorMercado'] = self.valorMercado
            info['acoesEmitidas'] = self.acoesEmitidas
            info['caixa'] = self.caixa
            info['lucroLiquido'] = self.lucroLiquido
            return info
        except:
            return 'ERRO INFO DATA'
    
    def Dy(self):
        temp_dy = 0
        lt = []
        info = {}
        if len(self.ticker) > 6:
            return 'ERRO TICKER LARGEST'
        import os
        import fundamentus
        df = fundamentus.get_resultado()
        for index in df.index:
            if index == self.ticker:
                if float(df['dy'][index]) == 0:
                    info['dy_actual'] = 0
                    info['dy6'] = 0
                    info['dy8'] = 0
                    info['dy10'] = 0
                    info['dy12'] = 0
                    info['actual_dy'] = 0
                else:
                    info['dy_actual'] = str(float(f"{df['dy'][index]:.2f}") * 100) + '%'
                    info['dy6'] = float((f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}"))
                    info['dy8'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.08:.2f}")
                    info['dy10'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.10:.2f}")
                    info['dy12'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.12:.2f}")
                    info['actual_dy'] = f"{((df['cotacao'][index])*(df['dy'][index]))/df['dy'][index]:.2f}"
                    if df['dy'][index] > 15 and df['dy'][index] < 20:
                        temp_dy = df['dy'][index] - 5
                    if df['dy'][index] > 20:
                        temp_dy = df['dy'][index] - 10
                    else:
                        temp_dy = df['dy'][index]
                    info['dpa'] = (float((df['cotacao'][index] - (temp_dy* df['cotacao'][index]))/df['cotacao'][index]) * 10)
                return info
            
    def Margin(self):
        try:
            margin = ((self.Dy()['dpa'])/self.Datas()['value'] -1)*100
            if margin < 0:
                margin = margin * -1
                return float(f'{margin:.2f}')
            return float(f'{margin:.2f}')
        except:
            return 0
            
    def getImage(self):
        self.soup = self.Soup()
        
        try:
            if self.soup.find('div', title="Logotipo da empresa '" + self.Datas()['name']) != None:
                getImagee = self.soup.find("div", title="Logotipo da empresa '"+self.Datas["name"].upper()+"'")
                return "https://statusinvest.com.br" +getImagee.__str__().split("(")[1].split(")")[0]
            else:
                for x in self.soup.find_all("div"):
                    if str(x).__contains__("data-img"):
                        try:
                            print("https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0])
                            return "https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0]
                        except:
                            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
                return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
        except:
            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

    def getImageDetalhes(self):
        soup = self.SoupP()
        try:
            if soup.find('img',attrs={'id': 'imgFoto'}) :
                img = soup.find('img',attrs={'id': 'imgFoto'})
                return img['src']
            else:
                return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
        except:
            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
        
    @staticmethod
    def variacoes():
        data = [[],[],[],[]]

        def Soup():

            b = Browser()
            b.set_handle_robots(False)
            b.addheaders = [('Referer', 'https://statusinvest.com.br'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
            b.open('https://statusinvest.com.br')
            page = b.response().read()
            soup = BeautifulSoup(page, "lxml")
            return soup
            
        soup = Soup()
        if soup == 'ERRO SOUP': return

        dados = soup.findAll('div', attrs={'class': 'w-100 w-sm-50 w-xl-25 mt-4 mt-xl-0'})

        altas = dados[0]
        identificadoresAlta = altas.findAll('h4', {'title': 'ticker/código do ativo'})
        valoresAcaoAlta = altas.findAll('span', {'class': 'd-flex fw-900 other-value'})
        variacaoAcaoAlta = altas.findAll('span', {'class': 'value align-items-center d-flex'})  
        imagensAlta = altas.findAll('div', {'class': 'avatar'})

        
        for i in range(len(identificadoresAlta)):
            urlImg = (str(imagensAlta[i])).split('"')[3].split('(')[1].replace(')', '')
            data[0].append({
                'ticker' : identificadoresAlta[i].text.split(' ')[0],
                'name': identificadoresAlta[i].text.split(' ')[1],
                'value': formate_Number(valoresAcaoAlta[i].text.split('"')),
                'volatility': formate_Number(variacaoAcaoAlta[i].text),
                'url-image': f'https://statusinvest.com.br{urlImg}'
            })

        baixas = dados[1]
        identificadoresBaixa = baixas.findAll('h4', {'title': 'ticker/código do ativo'})
        valoresAcaoBaixa = baixas.findAll('span', {'class': 'd-flex fw-900 other-value'})
        variacaoAcaoBaixa = baixas.findAll('span', {'class': 'value align-items-center d-flex'})  
        imagensBaixa = baixas.findAll('div', {'class': 'avatar bg-lazy'})

        for i in range(len(identificadoresBaixa)):
            urlImg = (str(imagensBaixa[i])).split('"')[3].split('(')[1].replace(')', '')
            data[1].append({
                'ticker' : identificadoresBaixa[i].text.split(' ')[0],
                'name': identificadoresBaixa[i].text.split(' ')[1],
                'value': formate_Number(valoresAcaoBaixa[i].text.split('"')),
                'volatility': formate_Number(variacaoAcaoBaixa[i].text),
                'url-image': f'https://statusinvest.com.br{urlImg}'
            })

        dividendos = dados[2]
        identificadoresDividendos = dividendos.findAll('h4', {'title': 'ticker/código do ativo'})
        valoresDividendo = dividendos.findAll('span', {'class': 'value align-items-center d-flex'})
        tipoDividendo = dividendos.findAll('span', {'class': 'tag'})  
        dataDividendo = dividendos.findAll('span', {'class': 'd-block fs-2 lh-2 w-md-50 w-xl-100 fw-700'})
        imagensDivindendo = dividendos.findAll('div', {'class': 'avatar bg-lazy'})
        
        for i in range(len(identificadoresDividendos)):
            urlImg = (str(imagensDivindendo[i])).split('"')[3].split('(')[1].replace(')', '')
            data[2].append({
                'ticker' : identificadoresDividendos[i].text.split(' ')[0],
                'name': identificadoresDividendos[i].text.split(' ')[1],
                'value': formate_Number(valoresDividendo[i].text, 4),
                'type': tipoDividendo[i].text,
                'date': dataDividendo[i].text.replace('\n', ''),
                'url-image': f'https://statusinvest.com.br{urlImg}'
                
        })
        
        comunicados = dados[3]
        identificadoresComunicados = comunicados.findAll('h4', {'title': 'ticker/código do ativo'})
        imagensComunicado = comunicados.findAll('div', {'class': 'avatar bg-lazy'})
        amount = comunicados.findAll('span', {'class': 'quantity rounded d-inline-block fw-900'})
        typeComunicado = comunicados.findAll('div', {'class': 'main-info align-items-center d-flex justify-between'})
        urlComunicado = comunicados.findAll('div', {'class': 'info w-100'})

        for i in range(len(identificadoresComunicados)):
            ticker = identificadoresComunicados[i].text.split(' ')[0]
            urlImg = (str(imagensComunicado[i])).split('"')[3].split('(')[1].replace(')', '')
            data[3].append({
                'ticker' : ticker, 
                'name': identificadoresComunicados[i].text.split(' ')[1],
                'amount': amount[i].text,
                'url-image': f'https://statusinvest.com.br{urlImg}',
                'type': (typeComunicado[i].text).replace('\n' ,'').replace('1', '').replace('2', '').replace('comunicado novo/atualizado', 'comunicado').replace('comunicados novos/atualizados', 'comunicado'),
                # refazer a linha acima
                'url': f'https://statusinvest.com.br/acoes/{ticker}#go-document-section'
        })

        with open('./app/json/homeVar.json', 'w') as file:
            json.dump(data, file, indent=4)

        return data

a = BasicData('bbas3')
print(a.buyBack())