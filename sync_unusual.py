#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-10

@author: kplam
"""

import json,re,gzip
import kpfunc.function as kf
import kpfunc.getdata as kg
import kpfunc.spyder as ks
import pandas as pd



conn=kg.localconn()
filelist=kf.GetFileList('./data/unusual/')
print(filelist)
for file in filelist:
    with open(file,'rb') as f:
        zdata=f.read()
        data =gzip.decompress(zdata).decode('utf-8')
        df = pd.read_json(data,dtype='objcet')

        df['date'] = str(file[-13:-3])
        df['datetime'] = df['date'] + " " + df['time']
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df[['datetime', 'code', 'type', 'data', 'goodorbad']]
        # print(df)
        df.to_sql('unusual',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
