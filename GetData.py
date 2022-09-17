from bs4 import BeautifulSoup
import requests
import lxml
import cchardet
# Global Methods

def highdy():
        info = []
        try:
            import fundamentus
            df = fundamentus.get_resultado()
            maiores = df.nlargest(150,'dy')
            for index in maiores.index:
                if df['dy'][index] > 1 or df['dy'][index] < 0.06:
                    continue
                info.append(index)
            return info
        except:
            return 'ERRO HIGH DY'
        
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

# Classe de coleta de dados

class BasicData():
    
    def __init__(self,ticker) -> str:
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
        
        self.name = self.soup.findAll(attrs={'class':'lh-4'})[0].text
        try:
            self.value_class = self.soup.findAll(attrs={'class':'value'})
        except:
            return 'ERRO VALUE CLASS'

        self.value = self.value_class[0].text
        self.value = float(Formate_Number(self.value))
        self.dy_Value = self.value_class[3].text
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
            return 'ERRO DB BLOCK CLASS'
        self.p_vp = self.value_dblock_class[3].text
        self.roe = self.value_dblock_class[24].text
            
        try:
            info['name'] = self.name
            info['value'] = self.value
            info['dy_value'] = self.dy_Value
            info['dy_porcent'] = self.dy_Porcent
            info['p_vp'] = self.p_vp
            info['roe'] = self.roe
            info['tag_along'] = self.tagAlong
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
                info['dy6'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}")
                info['dy8'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.08:.2f}")
                info['dy10'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.10:.2f}")
                info['dy12'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.12:.2f}")
                info['actual_dy'] = f"{(df['cotacao'][index])*(df['dy'][index])/df['dy'][index]:.2f}"
                return info
            
    def Margin(self):
        try:
            margin = (self.Dy()['dy6']/self.Datas()['value'] -1)*100
            return f'{margin:.2f}' + '%'
        except:
            return 'ERRO MARGIN'