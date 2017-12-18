# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on 15:20:00 2017-12-16
@author: kplam
"""

import pandas as pd
from kpfunc.getdata import localconn,serverconn

def pjgj(conn=localconn()):
    try:
        query = "select `date` from `indexdb` WHERE `code`='880003' ORDER by `date` DESC limit 1"
        lastdate = pd.read_sql(query,conn).values
        print(lastdate)
        table = pd.read_csv('./data/pjgj/880003.csv',encoding='gbk',header=None,names=['date','open','high','low','close','vol','amo'])
        table = table[:len(table)-1]
        table['date'] = table['date'].astype('datetime64')
        table['code'] = '880003'
        table = table[table['date']>lastdate[0][0]].reset_index(drop=True)
        table.to_sql('indexdb',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pjgj(conn=localconn())
    pjgj(conn=serverconn())

