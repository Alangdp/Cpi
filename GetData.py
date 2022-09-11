from ast import For
from bs4 import BeautifulSoup
import html5lib
import requests


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
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html5lib')
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
            self.value = self.soup.findAll(attrs={'class':'value'})[0].text
            self.value = float(Formate_Number(self.value))
        except:
            return 'ERRO VALUE'
        try:
            self.dy_Value = self.soup.findAll(attrs={'class':'sub-value'})[3].text
            self.dy_Value = Formate_Number(self.dy_Value)
        except:
            return 'ERRO DY_VALUE'
        try:
            self.dy_Porcent = self.soup.findAll(attrs={'class':'value'})[3].text
            if str(self.dy_Porcent) == '-':
                self.dy_Porcent = '0.01'
            else:
                self.dy_Porcent = Formate_Number(self.dy_Porcent)
        except:
            return 'ERRO DY_PORCENT'
        try:
            self.tagAlong = self.soup.findAll(attrs={'class':'value'})[6].text
        except:
            return 'TAG_ALONG'
        try:
            self.p_vp = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})[3].text
        except:
            return 'ERRO P_VP'
        try:
            self.roe = self.soup.findAll(attrs={'class':'value d-block lh-4 fs-4 fw-700'})[24].text
        except:
            return 'ERRO ROE'
            
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
        
    def Dy(self):
        lt = []
        info = {}
        if len(self.ticker) > 6:
            return 'ERRO TICKER LARGEST'
        import os
        import fundamentus
        df = fundamentus.get_resultado()
        for index in df.index:
            if index == self.ticker:
                info['dy6'] = float(f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}")
                info['dy8'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}")
                info['dy10'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}")
                info['dy12'] = (f"{df['cotacao'][index]*(df['dy'][index])/0.06:.2f}")
                info['actual_dy'] = f"{self.Datas()['dy_value']/df['dy'][index]:.2f}"
                try:
                    info['margin'] = f"{((info['dy6']/df['cotacao'][index]) - 1) * 100:.2f}"
                except:
                    return 'ERRO MARGIN'
                return info
    
    def Margin(self):
        try:
            margin = (self.Dy()['dy6']/self.Datas()['value'] -1)*100
            return f'{margin:.2f}' + '%'
        except:
            return 'ERRO MARGIN'