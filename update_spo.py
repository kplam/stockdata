#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""
from kpfunc.spyder import spyder
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
from numpy import nan
from time import sleep
from random import random
import datetime
import pandas as pd
import json,re

def spo(conn=localconn(),proxy=0):
    errorlist=[]
    today=datetime.date.today()
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=50&st=5"
    html = spyder(url,proxy=proxy).content
    table = eval(html.decode('utf-8'))
    list =[]
    for ele in table:
        list.append(re.split("\,",ele))
    df_spo = pd.DataFrame(list,columns=['code','name','发行方式','发行总数','发行价格','现价','发行日期','增发上市日期',
                                        '8','增发代码','网上发行','中签号公布日','中签率','13','14','15','16'])
    df_spo = df_spo[['code','name','发行方式','发行总数','发行价格','发行日期','增发上市日期','增发代码','网上发行',
                     '中签号公布日','中签率']]
    df_spo = df_spo.drop_duplicates()
    df_spo = df_spo.replace('-',nan)
    # print(df_spo)

    df_spo['发行日期']=df_spo['发行日期'].astype('datetime64')
    spo=df_spo[df_spo['发行日期']==today]
    spo.to_csv(path() + '/data/spo_done/spo_' + str(today) + '.csv',encoding='utf-8')
    try:
        spo.to_sql('spo_done',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
    except Exception as e:
        print(e)
        errorlist.append(e)
    return errorlist

""" 
"http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=50&st=5"
"""
if __name__ =="__main__":
    errorlist=spo(conn=localconn(),proxy=0)
    df=pd.DataFrame(errorlist)
    df.to_csv(path()+'/error/update_spo.csv')
