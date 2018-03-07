#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22

@author: kplam
"""
from kpfunc.spyder import myspyder
from kpfunc.getdata import *
from kpfunc.function import path
from time import sleep
from random import random
import datetime
import pandas as pd
import json,re

"""
http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?tkn=eastmoney&mkt=0&dateNum=&startDateTime=2018-03-01&endDateTime=2018-03-01&sortRule=1&sortColumn=&pageNum=1&pageSize=200&cfg=lhbggdrtj
"""


def get_lhblist(date,proxy):
    url_sh="http://stock.jrj.com.cn/action/lhb/getHsTodaylhb.jspa?vname=list&date=%s&dateType=2&order=desc&sort=netvalue_value&psize=2000"%(date)
    html_sh = myspyder(url_sh,proxy=proxy).content.decode('utf-8')#[9:-3]
    url_sz ="http://stock.jrj.com.cn/action/lhb/getHsTodaylhb.jspa?vname=list&date=%s&dateType=1&order=desc&sort=netvalue_value&psize=2000"%(date)
    html_sz = myspyder(url_sz,proxy=proxy).content.decode('utf-8')#[9:-3]
    lhblist = list(set(re.findall('\d{6}',html_sh)+re.findall('\d{6}',html_sz)))
    return lhblist

def get_lhbdetail(code,date,proxy):
    url = "http://stock.jrj.com.cn/action/lhb/getStockLhbDetatil.jspa?vname=detailInfo&stockcode=%s&date=%s"%(code,date)
    html = myspyder(url,proxy=proxy).content.decode('utf-8')
    html = re.split("\;",html)
    json_detail = html[0][15:]
    j=1
    while json_detail[-1] != "}":
        json_detail = json_detail+html[j]
        j=j+1
    # else:
    #     json_detail =  html[0][15:]
    data = json.loads(json_detail)['data']
    df_detail =pd.DataFrame()
    for i in range(len(data)):
        tmp_detail = pd.DataFrame(data[i][1],columns=['date', 'code', '买入金额', '卖出金额', '净买入金额', '净买入金额占总成交额', 'pl', '上榜原因', '买卖方向', '营业部代码', '营业部名称', '买入金额占总成交额', '卖出金额占总成交额', '上榜总成交额'])
        df_detail = pd.concat((tmp_detail,df_detail))
    return df_detail

def lhb():
    # sql_date = "select distinct `date` from `indexdb` WHERE `date`>='2017-01-01' ORDER BY `date` ASC "
    # list_date = pd.read_sql(sql_date,localconn())['date'].values
    print("LHB:正在获取成交回报信息...")
    today =datetime.date.today()
    list_date=[today]
    errorlist =[]
    for date in list_date:
        df_lhbdetail = pd.DataFrame()
        try:
            lhb_list = get_lhblist(str(date),proxy=0)
            print(str(date),len(lhb_list))
            if len(lhb_list) ==0:
                errorlist.append((str(date),0))
            for code in lhb_list:
                # print(str(date),code)
                tmp_lhbdetail = get_lhbdetail(code,str(date),proxy=0)
                # tmp_lhbdetail =tmp_lhbdetail.drop_duplicates()
                df_lhbdetail = pd.concat((tmp_lhbdetail,df_lhbdetail))
                sleep(random()/10+1)
        except Exception as e:
            errorlist.append((str(date),code,e))
        df_lhbdetail.to_csv('./data/lhb/'+str(date)+'.csv',encoding='utf-8')
        try:
            df_lhbdetail.to_sql('lhb',conn(),schema='stockdata',if_exists='append',
                                index=True,chunksize=10000)
        except Exception as e:
            print(e)

    df_error = pd.DataFrame(errorlist)
    df_error.to_csv(path()+'/data/lhb/error.csv')
    print("LHB:更新完毕！")

if __name__ == "__main__" :
    lhb()
