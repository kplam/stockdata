#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
from kpfunc.spyder import *
from kpfunc.getdata import localconn,serverconn
import datetime
import pandas as pd
from time import sleep
from random import random
from numpy import nan

def get_blocktrade(list_date,ser=localconn(),proxy=0):
    list_date_error=[]
    for date in list_date:
        try:
            print(str(date))
            url="http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=DZJYXQ&token=70f12f2f4f091e459a279469fe49eca5&cmd=&p=1&ps=500&st=st=SECUCODE&sr=1&filter=(TDATE=^%s^)&rt=50385715"%(str(date))
            data =myspyder(url,proxy=proxy).content.decode('utf-8')
            list = pd.read_json(data,orient='table',dtype={'SECUCODE':str})
            list = list.values
            list = pd.DataFrame(list,columns=['买方代码','买方营业部','收盘价','成交额流通市值占比','成交价','涨跌幅','10日涨跌幅','次日涨跌幅','20日涨跌幅','5日涨跌幅','卖方代码','卖方营业部','code','name','类型','交易日期','市场','成交额','成交量','单位','YSSLTAG','折价率'])
            list['折价率'] = list['折价率'] * 100
            list = list[['code','name','交易日期','买方代码','买方营业部','收盘价','成交价','涨跌幅','卖方代码','卖方营业部','类型','市场','成交额','成交量','单位','YSSLTAG']]
            list = list.replace('-',nan)
            list['收盘价']=list['收盘价'].astype(float)
            list['交易日期'] = list['交易日期'].astype('datetime64')
            list.to_csv('./data/blocktrade/'+str(date)+'.csv')
            list.to_sql('blocktrade',ser,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
            sleep(random()/10+3)
        except Exception as e:
            print(str(date),e)
            list_date_error.append(str(date))
    return list_date_error

if __name__ == "__main__" :
    today = datetime.date.today()
    # sql_date = "select distinct `date` from `indexdb` where `date`>'2013-10-01' ORDER BY `date` ASC "
    # list_date = pd.read_sql(sql_date,conn)['date'].values
    list_date = [today]
    times_retry = 3
    error = get_blocktrade(list_date=list_date,ser=localconn(),proxy=0)
    while len(error) != 0 and times_retry != 0:
        error = get_blocktrade(list_date=error,ser=localconn(),proxy=0)
        times_retry -= 1