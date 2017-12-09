#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-09

@author: kplam
"""

"""
http://nuyd.eastmoney.com/EM_UBG_PositionChangesInterface/api/js?style=top&js=[(x)]&ac=normal&dtformat=HH:mm:ss
"""
from kpfunc.spyder import spyder
from kpfunc.function import path
import datetime,json,re,gzip
import pandas as pd
def unusual():
    url = "http://nuyd.eastmoney.com/EM_UBG_PositionChangesInterface/api/js?style=top&js=[(x)]&dtformat=HH:mm:ss&ac=normal"
    html = spyder(url,0).content.decode('utf-8')
    return html
def analysis():
    today = datetime.date.today()
    data = json.loads(unusual())
    table = [re.split(",",ele) for ele in data]
    for elem in table:
        elem[0]= elem[0][:-1]
    df = pd.DataFrame(table,columns=['code','name','time','tcode','type','data','goodorbad'])
    js = df.to_json(orient='records',force_ascii= False).encode('utf-8')
    with open(path()+"./data/unusual/"+str(today)+".jz",'wb') as f:
        f.write(gzip.compress(js,compresslevel=9))
    return df
if __name__ == '__main__':
    df = analysis()
    print(df[df['type']=='大笔买入'])