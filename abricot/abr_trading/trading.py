import requests
import bs4
import pandas as pd
import json 

def get_trading_data(stock_id,time_start,time_end):
    #取得結構
    res=requests.get(f'https://histock.tw/stock/branch.aspx?no={stock_id}&from={time_start}&to={time_end}')
    #更改資料的字元編碼
    res.encoding = 'big-5'

    #使用bs4的BeautifulSoup
    soup = bs4.BeautifulSoup(res.text,"html.parser")
    #找到table
    data = soup.select('table')[0]
    #使用read_html建立DataFrame
    df = pd.read_html(data.prettify())
    dfs = df[0]
    return dfs

def dataframe_to_json(df,orient='split'):
    df_json = df.to_json(orient = orient, force_ascii = False)
    return json.loads(df_json)


"""
# test
df=trading_table=get_trading_data('2330',20230101,20230110)
jason1=dataframe_to_json(df)
print(df)
print(jason1)
"""