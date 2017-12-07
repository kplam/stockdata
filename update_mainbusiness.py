#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""
from kpfunc.spyder import spyder
from kpfunc.getdata import localconn,serverconn,get_stocklist_prefix,local2conn
from kpfunc.function import path
from time import sleep
from random import random
import pandas as pd
from numpy import nan
import json


def mainbusiness(stocklist=get_stocklist_prefix('sh','sz',1),conn=localconn(),proxy=0):
    url = "http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code="
    errorlist =[]
    for code in stocklist:
        print(code)
        try:
            html = spyder(url+code,proxy=proxy)
            js = json.loads(html.content)
            with open("./data/mainbusiness/"+code[2:]+".json",'w',encoding='utf-8') as f:
                f.write(str(html.content,encoding='utf-8'))
            # print(js['zyfw'][0]['ms'])
            # print(js['jyps'][0]['ms'])
            table =[]
            for line in js['zygcfx']:
                listcp = [list(line['cp'][i].values()) + ['产品'] for i in range(len(line['cp']))]
                listhy = [list(line['hy'][i].values()) + ['行业'] for i in range(len(line['hy']))]
                listqy = [list(line['qy'][i].values()) + ['地区'] for i in range(len(line['qy']))]
                list_all = listcp + listhy + listqy
                table = table + list_all
            df = pd.DataFrame(table,columns=['报表日期','主营构成','主营收入(元)','收入比例','主营成本(元)','成本比例',
                                              '主营利润(元)','利润比例','毛利率(%)','9','主营收入','分类'])
            df['code']=code[2:]
            df= df[['code','报表日期','主营构成','主营收入','收入比例','主营成本(元)','成本比例',
                                              '主营利润(元)','利润比例','毛利率(%)','分类']].values
            for i in range(len(df)):
                df[i][4] = df[i][4].replace('%', '')
                df[i][6] = df[i][6].replace('%', '')
                df[i][8] = df[i][8].replace('%', '')
                df[i][9] = df[i][9].replace('%', '')
                if '亿' in df[i][5]:
                    df[i][5] = float(df[i][5].replace('亿', '')) * 100000000
                elif '万' in df[i][5]:
                    df[i][5] = float(df[i][5].replace('万', '')) * 10000
                if '亿' in df[i][7]:
                    df[i][7] = float(df[i][7].replace('亿', '')) * 100000000
                elif '万' in df[i][7]:
                    df[i][7] = float(df[i][7].replace('万', '')) * 10000
            df = pd.DataFrame(df, columns=['code','报表日期','主营构成','主营收入','收入比例','主营成本','成本比例',
                                              '主营利润','利润比例','毛利率','分类'])
            df = df.replace('--', nan)
            # print(df)
            df.to_sql('mainbusiness',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
        except Exception as e:
            print(e)
            errorlist.append(code)
        sleep(random()/10+1)
    return errorlist
"""
主营分析：http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code=sh603533
"""
if __name__ == "__main__":
    stocklist = get_stocklist_prefix('sh','sz',1)
    times_retry = 3
    while len(stocklist) != 0 and times_retry != 0:
        stocklist = mainbusiness(stocklist,localconn(),0)
        times_retry -= 1
    error=pd.DataFrame(stocklist)
    error.to_csv(path()+'/error/update_mainbusiness.csv')