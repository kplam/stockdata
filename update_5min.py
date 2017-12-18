from kpfunc.getdata import get_stocklist
import pandas as pd

table = pd.read_csv('./data/5m/000001.csv',encoding='gbk',header=None,names=['date','time','open','high','low','close','vol','amo'])
table =table[:len(table)-1]
# table['date'] =table['date'].astype('datetime64[ns]')

print(table)
list = []
for i in range(len(table)):
    datetime =str(table['date'][i])+" "+("0000"+str(table['time'][i])[:-4]+":"+str(table['time'][i])[-4:-2]+":00")[-8:]
    open = table['open'][i]
    high = table['high'][i]
    low = table['low'][i]
    close = table['close'][i]
    vol = table['vol'][i]
    amo = table['amo'][i]
    list.append([datetime,open,high,low,close,vol,amo])
table = pd.DataFrame(list,columns=['datetime','open','high','low','close','vol','amo'])
table['datetime'] =table['datetime'].astype('datetime64[ns]')
print(table)

