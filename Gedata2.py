from bs4 import BeautifulSoup
from mechanize import Browser
from extras import comandoSQL
from lxml import etree
import datetime
import fundamentus, lxml, shutil, requests, json, datetime, re, statistics

def formate_Number(x, virgulas = 2):
    try:
        x = re.sub(r'[^0-9.,]', '', x).strip()
        formated = float(x.replace(',', '.'))
        return float(f'{formated:.2f}')
    except:
        x = x.replace(',', '.').replace('.', '')
        return float(x.replace(",", ".").replace(" M", "")) * 10


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
        data = stock.data
        dy = stock.dividend

        info = {
            'ticker':stock.ticker,
            'name':data['name'],
            'value':data['value'],
            'dy_porcent':data['dy_porcent'],
            'dy_value':data['dy_value'],
            'tag_along':data['tag_along'],
            'roe':data['roe'],
            'margin':float(stock.margin()),
            'dy6':dy['dy6'],
            'dpa':dy['dy6'],
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
        self.dividends = self.requestApiStatus(f'https://statusinvest.com.br/acao/companytickerprovents?companyName=bancobrasil&ticker={self.ticker}&chartProventsType=1')

        try:
            self.value_dblock_class = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})
            self.value_class = self.soup.findAll(attrs={'class':'value'})
            self.strong_class = self.soup.findAll('strong',attrs={'class':'value'})
            self.value_sub_class = self.soup.findAll('span' ,attrs={'class':'sub-value'})
        except:
            pass

        self.data = self.datas()
        self.fundamentalData = self.fundamentalDatas()
        self.dividend = self.dy()

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

        info['dy_actual'] = f"{self.data['dy_value'] / (self.data['dy_porcent'] / 100):.2f}"
        info['dy6'] = self.data['dy_value'] / 0.06
        info['dy8'] = self.data['dy_value'] / 0.08
        info['dy10'] = self.data['dy_value'] / 0.010
        info['dy12'] = self.data['dy_value'] / 0.012
        lucroLiquido = self.cashFlow['data']['grid'][3]['columns']
        mediaLiquidaPorcent = self.cashFlow['data']['grid'][3]['columns']
        lucroLiquidoAtual = formate_Number(self.cashFlow['data']['grid'][3]['columns'][1]['value'])

        mediaLucroLiquido = statistics.mean([ formate_Number(valor['value']) for valor in lucroLiquido[1::2] ])
        mediaLiquidaPorcent = statistics.mean([ float((valor['value']).replace(',', '.')) for valor in lucroLiquido[2::2] ])

        info['lucroLiquidoMediaValue'] = mediaLucroLiquido
        info['lucroLiquidoMediaPorcent'] = mediaLiquidaPorcent
        info['lucroLiquidoProjetado'] = mediaLucroLiquido * (1 + mediaLiquidaPorcent / 100)

        return info
    
    def fundamentalDatas(self, *args):
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
        self.end_value = self.soupP.find('span', id="lbUltimoFechamento").text
        requestAtivos = self.assets
        caixa = requestAtivos['data']['grid'][4]['gridLineModel']['values'][0]
        self.caixa = f"{caixa:,.0f}"
        fluxoCaixa = self.cashFlow
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
            info['acoesEmitidas'] = int(formate_Number(self.acoesEmitidas))
            info['caixa'] = self.caixa
            info['lucroLiquido'] = self.lucroLiquido
            return info
        except:
            return 'ERRO INFO DATA'
    
    def margin(self, *args):
        precoTeto = self.dividend['dy6']
        valor = self.data['value']
        margin = (precoTeto - valor) / precoTeto * 100
        if margin < 0:
            margin = margin * -1
            return float(f'{margin:.2f}')
        return float(f'{margin:.2f}')
        
    def getImage(self):
        soup = self.soup

        if soup.find('div', title="Logotipo da empresa '" + self.data['name']) != None:
            getImagee = soup.find("div", title="Logotipo da empresa '"+self.data['name'].upper()+"'")
            return "https://statusinvest.com.br" +getImagee.__str__().split("(")[1].split(")")[0]
        else:
            for x in soup.find_all("div"):
                if str(x).__contains__("data-img"):
                    try:
                        print("https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0])
                        return "https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0]
                    except:
                        return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

    def getImageDetalhes(self):
        soup = self.soupP
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

print(dataColect('bbas3'))