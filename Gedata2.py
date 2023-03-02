from bs4 import BeautifulSoup
from mechanize import Browser
from extras import comandoSQL
from lxml import etree
import datetime
import fundamentus, lxml, shutil, requests, json, datetime
from GetData import BasicData as BD

        
def formate_Number(x, virgulas = 2):
    lt = []
    for y in str(x):
        if y == ',':lt.append('.')
        if y.isnumeric(): lt.append(y)
        continue
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
    dataFrame = fundamentus.get_resultado()
    for index in dataFrame.index:  
        try:
            validDy = dataFrame['dy'][index] > 0.5 or dataFrame['dy'][index] < 0.06
            marginLiq = dataFrame['mrgliq'][index] >= 0

            stock = BD(index)
            margin = stock.Margin()
            data = stock.Data()

            if not (not validDy and marginLiq): continue
            if stock.Margin() > 100: continue
            if not (data['p_vp'] >= 1.5 and data['pl'] <= 15): continue
            if margin > 100: continue



            stock = BasicData(index)
            print(dataFrame['dy'][index], dataFrame['mrgliq'][index])
            if (( not (dataFrame['dy'][index]  > 0.5 or dataFrame['dy'][index] < 0.06)) and dataFrame['mrgliq'][index] >= 0):
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
