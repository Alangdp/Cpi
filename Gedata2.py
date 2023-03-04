from bs4 import BeautifulSoup
from mechanize import Browser
from extras import comandoSQL
from lxml import etree
import datetime
import fundamentus, lxml, shutil, requests, json, datetime, re
from GetData import BasicData as BD

def formate_Number(x, virgulas = 2):
    x = re.sub(r'[^0-9.,]', '', x).strip()
    formated = float(x.replace(',', '.'))
    return float(f'{formated:.2f}')

def sqlString(valor):
    try:
        string = ''.join(valor)
        return string
    except:
        return valor
    
def Filter():
    info = []
    dataFrame = fundamentus.get_resultado()
    for index in dataFrame.index:  
        try:
            validDy = dataFrame['dy'][index] > 0.5 or dataFrame['dy'][index] < 0.06
            marginLiq = dataFrame['mrgliq'][index] >= 0

            stock = BD(index)
            margin = stock.Margin()
            data = stock.Data()

            if not (not validDy and marginLiq): continue
            if margin > 100: continue
            if not (data['p_vp'] >= 1.5 and data['pl'] <= 15): continue
            if margin > 100: continue
            if data['payout'] <= 10: continue
            info.append()       
        except:
            continue
    select(info)

def select(lista):
    comandoSQL("UPDATE Acoes set filtered = ?", ("False",))
    for ticker in lista:
        comandoSQL("UPDATE Acoes set filtered = True WHERE ticker = ?", (ticker, ))

def selected():
    tickers = comandoSQL("SELECT ticker FROM Acoes WHERE filtered = ?", ("1",))
    infos = [comandoSQL("SELECT * FROM Acoes WHERE ticker = (?) ORDER BY CAST(margin as REAL)", (sqlString(tickerSet),)) for tickerSet in tickers]
    retornavel = [info[0] for info in infos]
    return retornavel

def dataColect(ticker):
    if any(i in ticker for i in ['33', '5']):
        return None

    try:
        stock = BD(ticker)
        data = stock.Datas()
        dy = stock.Dy()

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

        return info
    except:
        return None

def sqUpdate(data ):
    datas = list(data)
    comandoSQL("CREATE TABLE IF NOT EXISTS Acoes (ticker text, name text, value text, dy_porcent text, dy_value text, tag_along text, roe text, margin text, dy6 text, img text, dpa text)", ())
    for data in datas:
        if datas == None: continue
        comandoSQL("INSERT INTO Acoes VALUES(?,?,?,?,?,?,?,?,?,?,?)", (data['ticker'],data['name'],data['value'],data['dy_porcent'],data['dy_value'],data['tag_along'],data['roe'],data['margin'],data['dy6'],data['img'],data['dpa']   ))

def getLocalData():
    comandoSQL("SELECT * FROM Acoes ORDER BY CAST(margin AS REAL)", ())
    datas = comandoSQL("SELECT * FROM Acoes", ())
    tickers = [data for data in datas]
    return list(tickers)

# Classe de Scrap

class BD():

    def __init__(self, ticker ):
        if ticker is None:
            raise ValueError("Ticker não pode ser nulo.")

        self.ticker = ticker.upper()
        self.date = datetime.date.today()

        self.soup = self.soupStatus()
        self.soupP = self.soupGuia()
        self.payout = self.requestApiStatus(f'https://statusinvest.com.br/acao/payoutresult?code={self.ticker}&companyid=331&type=1')
        self.cashFlow = self.requestApiStatus(f'https://statusinvest.com.br/acao/getfluxocaixa?code={self.ticker}&type=0&futureData=true')
        self.assets = self.requestApiStatus(f'https://statusinvest.com.br/acao/getativos?code={self.ticker}&type=0&futureData=false&range.min=2017&range.max={self.date.year}')

        try:
            self.value_dblock_class = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})
            self.value_class = self.soup.findAll(attrs={'class':'value'})
            self.strong_class = self.soup.findAll('strong',attrs={'class':'value'})
            self.value_sub_class = self.soup.findAll('span' ,attrs={'class':'sub-value'})
        except:
            pass

        self.data = self.datas()
    def soupStatus(self):
        try:
            b = Browser()
            b.set_handle_robots(False)
            b.addheaders = [('Referer', 'https://statusinvest.com.br'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
            page = b.open(f'https://statusinvest.com.br/acoes/{self.ticker}').read()
            return BeautifulSoup(page, "lxml")
        except Exception as e:
            raise Exception(f"Erro ao obter soup: {str(e)}")
        finally:
            b.close()
        
    def soupGuia(self):
        try:
            session = requests.Session()
            page = session.get(f'https://www.guiainvest.com.br/raiox/{self.ticker}.aspx')
            soup = BeautifulSoup(page.text, "lxml")
            return soup
        except Exception as e:
            raise Exception(f"Erro ao obter soup: {e}")
        
    def requestApiStatus(self, url, *args):
        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'https://statusinvest.com.br/acao/'), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        b.open(url)
        data = json.loads(b.response().read())
        return data

    
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
        except Exception as e:
            return f'Erro ao obter buyback: {e}'
    
    def datas(self, *args):

        try:
            self.ri = self.soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow", "class": "waves-effect waves-light btn btn-small btn-secondary"})[0]["href"]
        except:
            self.ri = None

        self.name = self.soup.find('small').text
        self.value = self.value_class[0].text
        self.value = float(formate_Number(self.value))
        self.dy_Value = self.value_sub_class[3].text
        self.div_liq = self.strong_class[91].text
        self.div_brt = self.strong_class[89].text
        self.dy_Porcent = self.value_class[3].text
        self.tagAlong = self.value_class[6].text
        self.p_vp = self.value_dblock_class[3].text
        self.p_vp = formate_Number(self.p_vp)
        self.roe = self.value_dblock_class[24].text   
        self.pl = self.value_dblock_class[1].text
        self.pl = formate_Number(self.pl)
        self.divLiq_ebitda = self.soup.findAll('div', class_='d-flex align-items-center justify-between pr-1 pr-xs-2')[15]

        # Tratamento de dados vázios

        if str(self.dy_Porcent) == '-': self.dy_Porcent = 0
        self.dy_Porcent = formate_Number(self.dy_Porcent)

        print(self.dy_Value, self.dy_Porcent)
        if self.dy_Value == '-': self.dy_Value = 0
        self.dy_Value = formate_Number(self.dy_Value)

        if self.tagAlong == '-': self.tagAlong = 0
        self.tagAlong = formate_Number(self.tagAlong)

        # Montagem Dicionário
        
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
            info['payout'] = formate_Number(f'{self.payout["avg"]:.2f}')
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

    def dy(self, *args):
        info = {}

        print(self.data['dy_value'], (self.data['dy_porcent']))
        info['dy_actual'] = f"{self.data['dy_value'] / (self.data['dy_porcent'] / 100):.2f}"
        info['dy6'] = self.data['dy_value'] / 0.06
        info['dy8'] = self.data['dy_value'] / 0.08
        info['dy10'] = self.data['dy_value'] / 0.010
        info['dy12'] = self.data['dy_value'] / 0.012
        lucroLiquidoProjetado = self.assets

        info['teste'] = lucroLiquidoProjetado['data']['grid'][12]
        # info['dpa'] = f"{(ticker_info['cotacao'] - (temp_dy * ticker_info['cotacao'])) / ticker_info['cotacao'] * 10:.2f}"
            
        return info


a = BD('bbas3')
print(a.data)
print(a.dy())


        

