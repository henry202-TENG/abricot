#base
import numpy as np
import pandas as pd
from collections import Counter
import ssl
from copy import deepcopy


#visual
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import seaborn as sns
from matplotlib.font_manager import fontManager
from tqdm.notebook import tqdm
from tqdm import tqdm


#time
import datetime as dt
 
#finance
import yfinance as yf
import talib

#model
import sklearn
from sklearn.preprocessing import StandardScaler


### 一、资料载入
#data=yf.download('2330.TW','2021-01-01','2022-12-25')
data= yf.Ticker('2330.TW').history(period="max")

### 二、技術指標(KD、RSI、MACD、MOM)
data["rsi"] = talib.RSI(data["Close"], timeperiod=14)# type: ignore
data['macd'], data['macdsig'],data['macdhist'] = talib.MACD(data["Close"], fastperiod=12, slowperiod=26, signalperiod=9)# type: ignore
data['kdf'], data['kds'] = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=9,slowk_period=3,slowk_matype=1,slowd_period=3,slowd_matype=1)# type: ignore
data["mom"] = talib.MOM(data["Close"],timeperiod=15)# type: ignore

### 三、刪除空值與無用欄位
data = data.fillna(method="pad",axis=0)
data = data.dropna(axis=0)
#del data["Adj Close"]
del data["Dividends"]
del data["Stock Splits"]

### 四、買賣訊號：用移動平均結合動能指標來定義趨勢，簡單運用MA10 > MA20 且 RSI10 >RSI 20時，判斷為上升趨勢
data["short_mom"] = data["rsi"].rolling(window=10,min_periods=1,center=False).mean()
data["long_mom"] = data["rsi"].rolling(window=20,min_periods=1,center=False).mean()
data["short_mov"] = data["Close"].rolling(window=10,min_periods=1,center=False).mean()
data["long_mov"] = data["Close"].rolling(window=20,min_periods=1,center=False).mean()
# 標記Labels,上升趨勢標的為1，反之標記為0
data['label'] = np.where((data.short_mov > data.long_mov) & (data.short_mom > data.long_mom), 1, 0)
data = data.drop(columns=["short_mov"])
data = data.drop(columns=["long_mov"])
data = data.drop(columns=["short_mom"])
data = data.drop(columns=["long_mom"])
# 觀察資料分佈是否均匀
print(data['label'].value_counts())
'''
plt.title('imbalance distribution')
plt.xlabel('Up and down trends')
plt.ylabel('count')
plt.bar(['1','0'], data['label'].value_counts())
plt.show()
'''

### 五、資料前處理
# 資料標準化
X = data.drop('label', axis = 1)
X[X.columns] = StandardScaler().fit_transform(X[X.columns])
y = pd.DataFrame({"label":data.label})
# 切割成學習樣本以及測試樣本，比例為7：3
split = int(len(data)*0.7)
train_X = X.iloc[:split,:].copy()
test_X = X.iloc[split:].copy()
train_y = y.iloc[:split,:].copy()
test_y = y.iloc[split:].copy()
X_train, y_train, X_test, y_test = np.array(train_X), np.array(train_y), np.array(test_X), np.array(test_y)
# 將資料維度改成三維符合接下來模型所需
X_train = np.reshape(X_train, (X_train.shape[0],1,-1))
y_train = np.reshape(y_train, (y_train.shape[0],1,1))
X_test = np.reshape(X_test, (X_test.shape[0],1,-1))
y_test = np.reshape(y_test, (y_test.shape[0],1,1))

### LSTM 模型
from keras.models import Sequential    #引入Sequential函式
from keras.layers import Dense    #引入層數
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import BatchNormalization

# Sequential()順序模型
regressor = Sequential()    #定義模型
# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 32, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
regressor.add(BatchNormalization())
regressor.add(Dropout(0.35))
# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 32, return_sequences = True))
regressor.add(Dropout(0.35))
# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 32, return_sequences = True))
regressor.add(Dropout(0.35))
# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 32))
regressor.add(Dropout(0.35))
# Adding the output layer,units 設為 1
regressor.add(Dense(units = 1,activation="sigmoid"))    #激勵層
# Compiling
regressor.compile(optimizer = 'adam', loss="binary_crossentropy",metrics=["accuracy"])
print(regressor.summary())

### 模型結果(訓練集)
# 將epochs 設定為100次
train_history = regressor.fit(X_train,y_train,batch_size=200,epochs=100,verbose='2',validation_split=0.2)

### 模型評估:藉Model loss 圖可看出訓練過程中兩條線有收斂情形，顯示模型無過擬合
loss = train_history.history["loss"]
var_loss = train_history.history["val_loss"]
plt.plot(loss,label="loss")
plt.plot(var_loss,label="val_loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.title("model loss")
plt.legend(["train","valid"],loc = "upper left")
plt.show()

### 變數重要性:顯示MACD、台股平均本益比及RSI為重要特徵值.Permutation Feature Importance:https://christophm.github.io/interpretable-ml-book/feature-importance.html
results = []
print(' Computing LSTM feature importance...')
# COMPUTE BASELINE (NO SHUFFLE)
oof_preds = regressor.predict(X_test, verbose='0').squeeze()    #Remove axes of length one from a
baseline_mae = np.mean(np.abs(oof_preds-y_test))

results.append({'feature':'BASELINE','mae':baseline_mae})           

for k in tqdm(range(len(list(test_X.columns)))):
    # SHUFFLE FEATURE K
    save_col = X_test[:,:,k].copy()
    np.random.shuffle(X_test[:,:,k])
                        
    # COMPUTE OOF MAE WITH FEATURE K SHUFFLED
    oof_preds = regressor.predict(X_test, verbose='0').squeeze() 
    mae = np.mean(np.abs( oof_preds-y_test ))
    results.append({'feature':test_X.columns[k],'mae':mae})
    X_test[:,:,k] = save_col
print(results)


### 模型結果(測試集)
rate=regressor.evaluate(X_test, y_test,verbose='1')
print('loss:',rate[0])
print('accuracy:',rate[1])


