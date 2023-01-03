#base
import numpy as np
import pandas as pd
import yfinance as yf
import ssl

#visual
import matplotlib.pyplot as plt
import mplfinance as mpf
import seaborn as sns
 
#time
import datetime as datetime
 
#finance
import talib

class KDline:
    # Constructo
    def __init__(self,data,plot):
        # Create the name and salary attributes
        self.data,self.plot = data,plot
    
    # Define a class method from_str
    @classmethod
    def yf_kd(cls, stock_id,time_start,time_end):
        ssl._create_default_https_context = ssl._create_unverified_context
        df=yf.download(stock_id,time_start,time_end)
        df.index  = pd.DatetimeIndex(df.index)
        dfnew = df.drop(["Adj Close"],axis = 1)
        #KD指標最常用的週期為(9,3,3)，Ta-lib中預設為(5,3,3)，http://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
        dfnew['k'], dfnew['d'] = talib.STOCH(dfnew['High'], dfnew['Low'], dfnew['Close'], fastk_period=9,slowk_period=3,slowk_matype=1,slowd_period=3,slowd_matype=1)# type: ignore
        #布林通道参数
        dfnew["upper"],dfnew["middle"],dfnew["lower"] = talib.BBANDS(dfnew["Close"], timeperiod=20, nbdevup=2.1, nbdevdn=2.1, matype=0)# type: ignore
        
        data=dfnew
        ## KD指標視覺化+繪製布林通道
        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        add_plot =[mpf.make_addplot(dfnew[['upper','lower']],linestyle='dashdot'),
                mpf.make_addplot(dfnew['middle'],linestyle='dotted',color='y'),
                mpf.make_addplot(dfnew["k"],panel= 2,color="b"),
                mpf.make_addplot(dfnew["d"],panel= 2,color="r"),]
        kwargs = dict(type='candle', mav=(5,10), volume = True,figsize=(20, 10),title = stock_id, style=s,addplot=add_plot)
        plot=mpf.plot(dfnew, **kwargs)
        return cls(data,plot)


"""#測試格式
kd2330=KDline.yf_kd("2330.TW",'2022-10-11','2022-11-30')
print(kd2330.data)
print(kd2330.plot)
"""

