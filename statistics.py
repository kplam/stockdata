#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-25
@author: kplam
"""

import pandas as pd
from kpfunc.getdata import localconn,serverconn
import datetime

def cal_statistics(ser='both'):

    # sql_listdate = "select distinct `date` from `indexdb`"
    # listdate= pd.read_sql(sql_listdate,conn)['date'].values[-1]
    today=datetime.date.today()
    listdate=[today]
    sql_delisted = "select * from `stocklist` WHERE `交易状态`='-1'"
    stocklist_delisted =pd.read_sql(sql_delisted,localconn())['证券代码'].values

    date_delisted =[]
    for code in stocklist_delisted:
        sql_date_delisted ="Select `date` from `dayline` WHERE `code`='%s' ORDER by `date` DESC limit 1"%(code)
        date_delisted.append(pd.read_sql(sql_date_delisted,localconn())['date'][0])

    sat=[]
    for date in listdate:
        sql_ontrade = "select count(`code`) from `dayline` where `date`='%s'"%(str(date))
        ontrade  = pd.read_sql(sql_ontrade,localconn())['count(`code`)'][0]
        sql_total = "select count(`首发日期`) from `basedata` where `首发日期`<='%s' and `首发日期`>'1990-12-18'"%(str(date))
        total = pd.read_sql(sql_total,localconn())['count(`首发日期`)'][0]
        delisted = [x for x in date_delisted if (x+datetime.timedelta(days=1))<= date]
        sat.append([str(date),ontrade,total-len(delisted)-ontrade,total-len(delisted),len(delisted),total])

    sat=pd.DataFrame(sat,columns=['date','ontrade','halt','total','delisted','all_listed'])
    if ser == 'local' or ser == 'both':
        sat.to_sql('statistics',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False)
    if ser == 'server' or ser == 'both':
        sat.to_sql('statistics',serverconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False)

if __name__ == '__main__':
    cal_statistics(ser='both')
