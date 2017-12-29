#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-07

@author: kplam
"""
from kpfunc.spyder import *
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
import re,datetime
import pandas as pd
from time import sleep
from random import random
"""
http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=1&ps=1000
"""

def mo(pages,ser='both',proxy=0):
    today = datetime.date.today() #- datetime.timedelta(days=1)
    error=[]
    df=pd.DataFrame()

    for page in pages:
        print("MO:Page:",page)

        try:
            url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=%s&ps=5000"%(page)
            html = myspyder(url,proxy=proxy).content.decode('utf-8')[1:-1]
            sleep(random()/10+3)
            table = re.findall(r'\"([^"]+)\"',html)
            list = [re.split("\,",line) for line in table]
            list = pd.DataFrame(list,columns=['变动比例','董监高人员姓名','code','变动人','持股种类','日期','变动股数',
                                              '变动后持股数','成交均价','名称','变动人与董监高的关系',11,'变动方式',
                                              '变动金额','职务',15])
            list = list[['code','日期','变动人','持股种类','变动股数','变动后持股数','成交均价','变动人与董监高的关系',
                         '变动方式','变动金额','职务','变动比例','董监高人员姓名']]
            list.to_csv(path()+"/data/managerial_ownership/"+str(page)+".csv",encoding='utf-8')
            df = pd.concat((list,df),ignore_index=True)
        except Exception as e:
            print(e)
            error.append(page)

    df=df.drop_duplicates()
    df['日期']=df['日期'].astype('datetime64')
    df=df[df['日期']>=today]
    if df.empty != True:
        for elem in df.values:
            sql_update_managerial="INSERT IGNORE INTO `managerial`(`code`, `日期`, `变动人`, `持股种类`, `变动股数`, " \
                                  "`变动后持股数`, `成交均价`, `变动人与董监高的关系`, `变动方式`, `变动金额`, `职务`," \
                                  " `变动比例`, `董监高人员姓名`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            params = [str(param) for param in elem]

            if ser == 'local' or ser == 'both':
                conn = localconn()
                cur = conn.cursor()
                cur.execute(sql_update_managerial,params)
                conn.commit()
            # df.to_sql('managerial', conn, flavor='mysql', schema='stockdata', if_exists='append', index=False,
            #           chunksize=10000)
            if ser == 'server' or ser == 'both':
                conns = serverconn()
                curs = conns.cursor()
                curs.execute(sql_update_managerial, params)
                conns.commit()
                # df.to_sql('managerial',conns,flavor='mysql',schema='stockdata',if_exists='append',index=False,
                #           chunksize=10000)
    return error

if __name__ == '__main__':
    # pages = range(1,2)
    # times_retry=3
    # while len(pages)!=0 and times_retry!=0:
    #     pages = mo(pages)
    #     times_retry -= 1
    mo([1],ser='both',proxy=0)
