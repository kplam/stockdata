#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""
from kpfunc.spyder import myspyder
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
from numpy import nan
import datetime,re
import pandas as pd

def spo(ser='both',proxy=0):
    """
    http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=5000&st=5

    update the spo data from eastmoney.com to server and local.

    :param ser: local/server/both
    :param proxy: user proxy set proxy=1 if not proxy=0,default 0
    :return: errorlist
    """
    print("SPO: Running...")
    errorlist = []
    today = datetime.date.today() - datetime.timedelta(days=100)
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=1000&st=5"
    html = myspyder(url,proxy=proxy).content
    table = eval(html.decode('utf-8'))
    list =[]
    for ele in table:
        list.append(re.split("\,",ele))
    df_spo = pd.DataFrame(list,columns=['code','name','发行方式','发行总数','发行价格','现价','发行日期','增发上市日期',
                                        '8','增发代码','网上发行','中签号公布日','中签率','13','14','15','16'])
    df_spo = df_spo[['code','name','发行方式','发行总数','发行价格','发行日期','增发上市日期','增发代码','网上发行',
                     '中签号公布日','中签率']]
    df_spo = df_spo.drop_duplicates()
    # df_spo = df_spo.replace('-','')
    # print(df_spo)

    df_spo['发行日期']=df_spo['发行日期'].astype('datetime64')
    spo = df_spo[df_spo['发行日期']>=today]
    spo.to_csv(path() + '/data/spo_done/spo_' + str(today) + '.csv',encoding='utf-8')
    try:
        for elem in spo.values:
            sql_update_spo = "INSERT IGNORE INTO `spo_done`(`code`, `name`, `发行方式`, `发行总数`, `发行价格`, " \
                             "`发行日期`, `增发上市日期`, `增发代码`, `网上发行`, `中签号公布日`, `中签率`) VALUES" \
                             " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = []
            for param in elem:
                if param!='-' :
                    params.append(str(param))
                else:
                    params.append(None)

            if ser == 'local' or ser == 'both':
                conn = localconn()
                cur = conn.cursor()
                cur.execute(sql_update_spo,params)
                conn.commit()
                # spo.to_sql('spo_done',localconn(),flavor='mysql',schema='stockdata',if_exists='append',
                #            index=False,chunksize=10000)
            if ser == 'server' or ser == 'both':
                conns = serverconn()
                curs = conns.cursor()
                curs.execute(sql_update_spo, params)
                conns.commit()
                # spo.to_sql('spo_done',serverconn(),flavor='mysql',schema='stockdata',if_exists='append',
                #            index=False,chunksize=10000)
        print("SPO: Done!")
    except Exception as e:
        print("SPO:",e)
        errorlist.append(e)
    return errorlist

""" 
"http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=50&st=5"
"""
if __name__ == '__main__':
    errorlist = spo(ser='both',proxy=0)
    df = pd.DataFrame(errorlist)
    df.to_csv(path()+'/error/update_spo.csv')
