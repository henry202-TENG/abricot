## import model
import pandas as pd
import yfinance as yf
import ssl
# base
import pandas as pd
 
# visual
import matplotlib.pyplot as plt
import mplfinance as mpf
 
# time
import datetime as datetime

def stock_kline(stock_id):
    ## 取得股票
    time_start = input("輸入開始日期 : ")
    time_end = input("輸入結束日期 : ")
    ssl._create_default_https_context = ssl._create_unverified_context
    df=yf.download(stock_id,time_start,time_end)
    address = r"/Users/duzhiwen/stock/" + stock_id +" " + time_start + "~" + time_end + ".csv"
    df.to_csv(address)

    ## 繪製蠟燭 K線圖‘
    df.index  = pd.DatetimeIndex(df.index)
    dfnew_2330 = df.drop(["Adj Close"],axis = 1)
    #美化
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', mav=(5,10), volume=True, figratio=(20,15), figscale=1.2,title = stock_id, style=s)
    mpf.plot(dfnew_2330, **kwargs)

