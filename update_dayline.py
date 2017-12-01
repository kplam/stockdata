# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
from kpfunc.spyder import spyder
from kpfunc.getdata import *
from kpfunc.function import path
from time import sleep
from random import random
import datetime,re

# ======== Global define ========= #

today = datetime.date.today()
conn = localconn()
indexlist = get_indexlist_prefix('sh','sz',pre=1)
stocklist = get_stocklist_prefix('sh','sz',pre=1)
print(today)

def get_sina_daybar(stocklist,proxy):
    dayline=[]
    for i in range(len(stocklist)):
        print(stocklist[i])
        try:
            urlsina ="http://hq.sinajs.cn/list=%s"%(stocklist[i])
            lastbar = "error!"
            times_retry= 3
            while lastbar=="error!" and times_retry != 0:
                lastbar = spyder(urlsina,proxy=proxy)
                times_retry -=1
            return_list = re.findall("\"(.*?)\"", lastbar.content.decode('gbk'))
            lastbar_sp =return_list[0].split(',')
            lastbar_sp.append(stocklist[i][2:])
            dayline.append(lastbar_sp)
            sleep((random()/10+0.1))
        except:
            pass
    dayline = pd.DataFrame(dayline,columns=['name','open','preclose','close','high','low','e','f','vol','amo','g','h','I','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','date','aa','ab','code'])
    dayline = dayline[['code','date','high','open','low','close','vol','amo']]
    dayline['date'] = dayline['date'].astype('datetime64')
    dayline['close'] = dayline['close'].astype('float32')
    dayline['high'] = dayline['high'].astype('float32')
    dayline['low'] = dayline['low'].astype('float32')
    dayline['open'] = dayline['open'].astype('float32')
    dayline['vol'] = dayline['vol'].astype('float32')
    dayline['amo'] = dayline['amo'].astype('float32')
    dayline = dayline[dayline['vol']>0]
    return dayline

# =============== update index daybar ============== #

df_indexdaybar = get_sina_daybar(indexlist,proxy=0)
errorlist_index=[]
try:
    df_indexdaybar.to_sql('indexdb', con=conn, flavor='mysql', if_exists='append',index=False, index_label='date', dtype=None)
except Exception as e:
    print("local:",e)
    errorlist_index.append(("local:",e))
print("Update indexs daybar done!")
dfErrorList = pd.DataFrame({'error': errorlist_index})
dfErrorList.to_csv(path()+'/error/update_indexdaybar.csv')
print(dfErrorList)
# =============== update stock daybar ============== #
df_stockdaybar = get_sina_daybar(stocklist,proxy=0)
errorlist_stock=[]
try:
    df_stockdaybar.to_sql('dayline', con=conn, flavor='mysql', if_exists='append',index=False, index_label='date', dtype=None)
except Exception as e:
    print("local:",e)
    errorlist_stock.append(("local:",e))
print("Update stock daybar done!")
dfErrorList = pd.DataFrame({'error': errorlist_index})
dfErrorList.to_csv(path()+'/error/update_stockdaybar.csv')
print(dfErrorList)

# =============== update stock status ============== #

sql_index = "select * from `indexdb` WHERE `code`='000001' order by `date` desc limit 0,1"
df_index = pd.read_sql(sql_index,conn)
date_index = df_index.get_value(0,'date')
print("Updating stock status...")
for code in stocklist:
    sql_daybar = "select * from `dayline` where `code`='%s'order by `date` desc limit 0,1"%(code[2:])
    df_daybar = pd.read_sql(sql_daybar,conn)
    if df_daybar.empty ==False:
        date_daybar = df_daybar.get_value(0,'date')
        if date_daybar == date_index:
            sql_stocklist = "update `stocklist` set `交易状态`=1 where 证券代码='%s'"%(code)
        elif date_index > date_daybar:
            sql_stocklist = "update `stocklist` set `交易状态`=0 where 证券代码='%s'"%(code)
        else:
            sql_stocklist = "update `stocklist` set `交易状态`=9 where 证券代码='%s'"%(code)
    else:
        sql_stocklist = "update `stocklist` set `交易状态`=9 where 证券代码='%s'" % (code)
    cur = conn.cursor()
    cur.execute(sql_stocklist)
    conn.commit()
print('Update Stock Status Done!', today)

