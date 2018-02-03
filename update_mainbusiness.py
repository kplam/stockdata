#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""
from kpfunc.spyder import myspyder
from kpfunc.getdata import localconn,serverconn,get_stocklist_prefix,local2conn
from kpfunc.function import path
from time import sleep
from random import random
import pandas as pd
from numpy import nan
import json,warnings,datetime
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import gevent
from tenacity import retry
from tenacity import stop_after_attempt

@retry(stop=stop_after_attempt(7))
def update_mb_single(code):
    ser='both'
    proxy=0
    if ser == 'local' or ser == 'both':
        conn = localconn()
    if ser == 'server' or ser == 'both':
        conns = serverconn()
    print("MAINBUSINESS:",code)
    url = "http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code="

    try:
        html = myspyder(url+code,proxy=proxy)
        js = json.loads(html.content,encoding='utf-8')
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
            if '万亿' in df[i][5]:
                df[i][5] = float(df[i][5].replace('万亿', '')) * 1000000000000
            elif '亿' in df[i][5]:
                df[i][5] = float(df[i][5].replace('亿', '')) * 100000000
            elif '万' in df[i][5]:
                df[i][5] = float(df[i][5].replace('万', '')) * 10000
            if '万亿' in df[i][7]:
                df[i][7] = float(df[i][7].replace('万亿', '')) * 1000000000000
            elif '亿' in df[i][7]:
                df[i][7] = float(df[i][7].replace('亿', '')) * 100000000
            elif '万' in df[i][7]:
                df[i][7] = float(df[i][7].replace('万', '')) * 10000
        df = pd.DataFrame(df, columns=['code','报表日期','主营构成','主营收入','收入比例','主营成本','成本比例',
                                          '主营利润','利润比例','毛利率','分类'])
        df['报表日期']=pd.to_datetime(df['报表日期'])
        df = df[df['报表日期']>datetime.date(2001,1,1)]
        df = df[df['主营构成']!='']
        df = df[df['主营构成']!='--']
        df = df.replace('--', '')
        # print(df)
        # df.to_sql('mainbusiness',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
        try:
            for elem in df.values:
                sql_update= "insert ignore into `mainbusiness` (code, 报表日期, 主营构成, 主营收入, 收入比例, 主营成本," \
                            " 成本比例, 主营利润, 利润比例, 毛利率, 分类) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                params = []
                for param in elem:
                    if param != '':
                        params.append(str(param))
                    else:
                        params.append(None)
                if ser == 'local' or ser == 'both':

                    cur =conn.cursor()
                    cur.execute(sql_update,params)
                    conn.commit()
                if ser == 'server' or ser == 'both':
                    curs =conns.cursor()
                    curs.execute(sql_update,params)
                    conns.commit()
        except Exception as e:
            print("MAINBUSINESS:",code,e)
            return code
    except Exception as e:
        print("MAINBUSINESS:",e)
        return code

def mainbusiness(stocklist=get_stocklist_prefix('sh','sz',1)):

    gpool=Pool(20)
    tasks = [gpool.spawn(update_mb_single,code) for code in stocklist]
    gevent.joinall(tasks)
    errorlist = [task.values for task in tasks]
    print(errorlist)
    return errorlist
"""
主营分析：http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code=sh603533
"""
if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    stocklist = get_stocklist_prefix('sh','sz',1)
    # times_retry = 3
    # while len(stocklist) != 0 and times_retry != 0:
    stocklist = mainbusiness(stocklist)
    # times_retry -= 1
    error=pd.DataFrame(stocklist)
    error.to_csv(path()+'/error/update_mainbusiness.csv')