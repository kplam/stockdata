#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2018-02-05

@author: kplam
"""

from kpfunc.spyder import myspyder
from kpfunc.getdata import *
import pandas as pd
import datetime,json,re,time,random

"""
http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/20180202.js
http://home.flashdata2.jrj.com.cn/limitStatistic/dtForce/20170331.js
http://home.flashdata2.jrj.com.cn/limitStatistic/zt/20180202.js
"""
def zrzdt(stype,sdate):
    print(sdate,stype)
    strdate = sdate.strftime("%Y%m%d")
    url = "http://home.flashdata2.jrj.com.cn/limitStatistic/%s/%s.js" % (stype,strdate)
    engine = conn()
    try:
        html = myspyder(url,proxy=0)
        js = html.content.decode('gbk')
        js = js.replace('var zr_%s='%(stype),'').replace(';','')
        js = eval(js)['Data']
        df = pd.DataFrame(js,columns=['code','name','time','close','percentage','amo','amplitude','turnoverate','5day','pe','concept_e','concept'])
        del df['concept_e']
        del df['5day']
        df['time'] = str(sdate) + ' ' + df['time']

        try:
            df.to_sql('zrzdt', engine, schema='stockdata', if_exists='append', index=False)
        except Exception as e:
            print("local:%s[%s]"%(sdate,e))

        return df
    except Exception as e:
        print(sdate,e)
        return pd.DataFrame()


def zdtld(stype,sdate,ser='both'):
    strdate = sdate.strftime("%Y%m%d")
    url = "http://home.flashdata2.jrj.com.cn/limitStatistic/%sForce/%s.js" % (stype, strdate)
    engine = conn()
    try:
        html = myspyder(url,proxy=0)
        js = html.content.decode('gbk')
        js = re.findall(u'"Data":(.*)\};',js,re.DOTALL)[0]
        js = js.replace('Infinity', '0')
        js = json.loads(js)
        df = pd.DataFrame(js,columns=['code','name','close','percentage','fcb','flb','fdmoney','lasttime','firsttime','opentimes','amplitude','force'])
        df['firsttime'] = str(sdate) + ' ' + df['firsttime']
        df['lasttime'] = str(sdate) + ' ' + df['lasttime']
        if ser == 'local' or ser == 'both':
            try:
                df.to_sql('zdt', engine, schema='stockdata', if_exists='append', index=False)
            except Exception as e:
                print("local:%s[%s]"%(sdate,e))
        if ser == 'local' or ser == 'both':
            try:
                df.to_sql('zdt', engine, schema='stockdata', if_exists='append', index=False)
            except Exception as e:
                print("server:%s[%s]"%(sdate,e))
        return df
    except Exception as e:
        print(sdate,e)
        return pd.DataFrame()

def updatesql_all():
    # sql = "select DISTINCT `date` from indexdb ORDER BY `date` DESC "
    # datelist = pd.read_sql(sql,localconn())['date'].values
    datelist = [datetime.date.today()]
    for sdate in datelist:
        if sdate >= datetime.date(2015,9,8):
            stypelist = ['zt','dt']
            for stype in stypelist:
                zrzdt(stype,sdate)
                zdtld(stype,sdate)
            time.sleep(1+random.random())

if __name__ == '__main__':
    updatesql_all()
