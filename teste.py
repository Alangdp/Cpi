# import GetData
# from GetData import Formate_Number
# import pandas
# import fundamentus
# import json
# import sqlite3
# import os   
             
# def highdy():
#         info = []
#         import fundamentus
#         df = fundamentus.get_resultado()
#         maiores = df.nlargest(200,'dy')
#         for index in maiores.index: 
#             if len(info) == 65:
#                 break        
#             try:
#                 print(index, len(info))
#                 if (( not (df['dy'][index]  > 0.5 or df['dy'][index] < 0.06)) and df['mrgliq'][index] > 0) :
#                     print(index, 'etapa 1', len(info))
#                     stock = GetData.BasicData(index)
#                     if float(stock.Margin().replace('%','')) > 400:
#                             continue
#                     else:
#                         if stock.Datas()['p_vp'] <= 2 and stock.Datas()['pl'] <= 15:
#                             info.append(index)
#                             print(index, 'etapa2', len(info))
#             except:
#                 continue
#         return info

        
# def highList(list):
    
#     lt = []
#     for x in range(len(list)):
          
#         tic = list[x]
#         if '33' in tic:
#             continue
#         a = GetData.BasicData(tic)
#         acao = {
#             'ticker':a.ticker,
#             'name':a.Datas()['name'],
#             'value':a.Datas()['value'],
#             'dy_porcent':a.Datas()['dy_porcent'],
#             'dy_value':a.Datas()['dy_value'],
#             'tag_along':a.Datas()['tag_along'],
#             'roe':a.Datas()['roe'],
#             'margin':a.Margin(),
#             'dy6':a.Dy()['dy6'],
#             'img':a.getImage(),
#         }
        
#         lt.append(acao)
#     return lt

# def sqUpdate():
    
#     con = sqlite3.connect('TopStocks.db')
#     cur = con.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS Acoes (ticker text, name text, value text, dy_porcent text, dy_value text, tag_along text, roe text, margin text, dy6 text, img text)")
    
#     for x in (highList(highdy())):
#         cur.execute("INSERT INTO Acoes VALUES(?,?,?,?,?,?,?,?,?)", (x['ticker'],x['name'],x['value'],x['dy_porcent'],x['dy_value'],x['tag_along'],x['roe'],x['margin'],x['dy6'],x['img']   ))
#         con.commit()
        
#     con.close()

# def refreshSQ():
#     try:
#         os.remove('TopStocks.db')
#     except:
#         pass
#     sqUpdate()
    
# def Showsq():
    
#     con = sqlite3.connect('TopStocks.db')
#     cur = con.cursor()
    
#     cur.execute("SELECT ticker FROM Acoes")
#     for x in cur:
#         print(x)
#     con.close()

# def test():
#     info = []
#     import fundamentus
#     df = fundamentus.get_resultado()
#     maiores = df.nlargest(200,'dy')
#     for x in maiores.index:
#         info.append(x)
#     return info
        
# def getLocalData():
#     con = sqlite3.connect('TopStocks.db')
#     cur = con.cursor()
#     tickers = []

#     cur.execute("SELECT * FROM Acoes")
#     for x in cur:
#         tickers.append(x)
#     con.close()
#     return tickers

from numpy import var


variavel = '\n\nDívida líquida\nformat_quote\n\nR$\n180.369.000.000\n'
def formate_Detail(x):
    lt = []
    num_char = 0
    for y in str(x):
        num_char += 1
        
        if num_char % 3 == 0:
            lt.append('.')
        if y.isnumeric():
            lt.append(y)
        else: 
            pass
    formated = ''.join(lt)
    return str(formated)

print(formate_Detail(variavel))