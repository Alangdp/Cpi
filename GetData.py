from bs4 import BeautifulSoup
import requests
import lxml
import cchardet
import pandas
import fundamentus
import sqlite3
import os   
# Global Methods
        
def Formate_Number(x):
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
    return float(f'{formated:.2f}')

def highdy():
        info = []
        import fundamentus
        df = fundamentus.get_resultado()
        maiores = df.nlargest(250,'dy')
        for index in maiores.index: 
            if len(info) == 90:
                break        
            try:
                print(index, len(info))
                if (( not (df['dy'][index]  > 0.5 or df['dy'][index] < 0.06)) and df['mrgliq'][index] > 0) :
                    print(index, 'etapa 1', len(info))
                    stock = BasicData(index)
                    if float(stock.Margin().replace('%','')) > 400:
                            continue
                    else:
                        if stock.Datas()['p_vp'] <= 2 and stock.Datas()['pl'] <= 15:
                            info.append(index)
                            print(index, 'etapa2', len(info))
            except:
                continue
        return info

        
def highList(list):
    
    lt = []
    for x in range(len(list)):
          
        tic = list[x]
        if '33' in tic:
            continue
        a = BasicData(tic)
        acao = {
            'ticker':a.ticker,
            'name':a.Datas()['name'],
            'value':a.Datas()['value'],
            'dy_porcent':a.Datas()['dy_porcent'],
            'dy_value':a.Datas()['dy_value'],
            'tag_along':a.Datas()['tag_along'],
            'roe':a.Datas()['roe'],
            'margin':a.Margin(),
            'dy6':a.Dy()['dy6'],
            'img':a.getImage(),
        }
        
        lt.append(acao)
    return lt

def sqUpdate():
    
    con = sqlite3.connect('TopStocks.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Acoes (ticker text, name text, value text, dy_porcent text, dy_value text, tag_along text, roe text, margin text, dy6 text, img text)")
    
    for x in (highList(highdy())):
        cur.execute("INSERT INTO Acoes VALUES(?,?,?,?,?,?,?,?,?,?)", (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img']   ))
        con.commit()
        
    con.close()

def refreshSQ():
    try:
        os.remove('TopStocks.db')
    except:
        pass
    sqUpdate()
    
def Showsq():
    
    con = sqlite3.connect('TopStocks.db')
    cur = con.cursor()
    
    cur.execute("SELECT ticker FROM Acoes")
    for x in cur:
        print(x)
    con.close()
        
def getLocalData():
    con = sqlite3.connect('TopStocks.db')
    cur = con.cursor()
    tickers = []

    cur.execute("SELECT * FROM Acoes")
    for x in cur:
        tickers.append(x)
    con.close()
    return tickers

# Classe de coleta de dados

class BasicData():

    def __init__(self,ticker):
        if ticker == None:
            exit()
        else:
            self.ticker = ticker.upper()
        
    def Soup(self, args=None):
        try:
            link = BasicData(self.ticker)
            url = (link.links())
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
        
    def Datas(self, args=None):
        info = {}
        self.soup = self.Soup()
        
        self.name = self.soup.find('small').text
        try:
            self.value_class = self.soup.findAll(attrs={'class':'value'})
        except:
            return 'ERRO VALUE CLASS'
        
        try:
            self.value_sub_class = self.soup.findAll('span' ,attrs={'class':'sub-value'})
        except:
            return 'ERRO VALUE CLASS'

        self.value = self.value_class[0].text
        self.value = float(Formate_Number(self.value))
        
        self.dy_Value = self.value_sub_class[3].text
        if self.dy_Value == '-':
            self.dy_Value = 0
        self.dy_Value = Formate_Number(self.dy_Value)
        
        self.dy_Porcent = self.value_class[3].text
        if str(self.dy_Porcent) == '-':
            self.dy_Porcent = '0.01'
        else:
            self.dy_Porcent = Formate_Number(self.dy_Porcent)
            
        self.tagAlong = self.value_class[6].text
        if '-' in self.tagAlong:
            self.tagAlong = '0.00'

        try:
            self.value_dblock_class = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})
        except: 
            return 'ERRO DB BLOCK LH CLASS '

        self.p_vp = self.value_dblock_class[3].text
        self.p_vp = Formate_Number(self.p_vp)
        self.roe = self.value_dblock_class[24].text   
        self.pl = self.value_dblock_class[1].text
        self.pl = Formate_Number(self.pl)
        try:
            self.ri = self.soup.find_all("a", attrs={"rel": "noopener noreferrer nofollow", "class": "waves-effect waves-light btn btn-small btn-secondary"})[0]["href"]
        except:
            self.ri = None
        try:
            info['ticker'] = self.ticker
            info['name'] = self.name
            info['value'] = self.value
            info['dy_value'] = self.dy_Value
            info['dy_porcent'] = self.dy_Porcent
            info['p_vp'] = self.p_vp
            info['roe'] = self.roe
            info['tag_along'] = self.tagAlong
            info['pl'] = self.pl
            info['ri_page'] = self.ri
            
            return info
        except:
            return 'ERRO INFO DATAS'
        
    def fundamentalDatas(self):
        info = {}
        self.soup = self.Soup()
        try:
            self.strong_class = self.soup.findAll('strong', class_="value")
        except:
            return 'ERRO STRONG CLASS'
        
        self.valor_12 = self.strong_class[4].text
        self.min_12 = self.strong_class[2].text
        self.max_12 = self.strong_class[1].text
        
        info['valor_12'] = self.valor_12
        info['min_12'] = self.min_12
        info['max_12'] = self.max_12
        return info
    
    def Dy(self):
        
        info = {}
        if len(self.ticker) > 6:
            return 'ERRO TICKER LARGEST'
        import os
        import fundamentus
        df = fundamentus.get_resultado()
        for index in df.index:
            if index == self.ticker:
                info['dy_actual'] = str(float(f"{df['dy'][index]:.2f}") * 100) + '%'
                info['dy6'] = float((f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}"))
                info['dy8'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.08:.2f}")
                info['dy10'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.10:.2f}")
                info['dy12'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.12:.2f}")
                info['actual_dy'] = f"{(df['cotacao'][index])*(df['dy'][index])/df['dy'][index]:.2f}"
                return info
            
    def Margin(self):
        try:
            margin = ((self.Dy()['dy6'])/self.Datas()['value'] -1)*100
            return f'{margin:.2f}' + '%'
        except:
            return 0
        
    def getImage(self):
        self.soup = self.Soup()
        if self.soup.find('div', title="Logotipo da empresa '" + self.Datas()['name']) != None:
            getImagee = self.soup.find("div", title="Logotipo da empresa '"+self.Datas["name"].upper()+"'")
            return "https://statusinvest.com.br" +getImagee.__str__().split("(")[1].split(")")[0]
        else:
            for x in self.soup.find_all("div"):
                if str(x).__contains__("data-img"):
                    try:
                        print(str(x).split("(")[1].split(")")[0])
                        return "https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0]
                    except:
                        return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
             
