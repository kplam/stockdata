#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2018-02-07

@author: kplam
"""

from kpfunc.getdata import *
from kpfunc.spyder import myspyder
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime,re

def update_focussql(N=5):
    engine=conn()
    urllist = []
    for i in range(1, N):
        if i == 1:
            urllist.append("http://money.163.com/special/002557S6/newsdata_gp_index.js")
        else:
            page = "0" + str(i) if len(str(i)) == 1 else str(i)
            urllist.append("http://money.163.com/special/002557S6/newsdata_gp_index_%s.js" % (page))
    noticelist = []
    for url in urllist:
        html = myspyder(url, proxy=0)
        doc = html.content.decode('gbk')
        js = doc.replace('data_callback(', '').replace(')', '')
        js = eval(js)
        for i in range(len(js)):
            # titlelist.append([js[i]['title'],js[i]['time'],js[i]['docurl']])
            if '公告汇总' in js[i]['title']:
                noticelist.append([js[i]['title'], js[i]['time'], js[i]['docurl']])

    sql = "select `证券代码`,`证券简称` from `basedata`"
    stocklist = pd.read_sql(sql, engine)
    final = []
    for i, [title, stime, docurl] in enumerate(noticelist):
        print(i, title, stime, docurl)
        html = myspyder(docurl, proxy=0)
        doc = html.content
        soup = bs(doc, 'html5lib')
        result = soup.select('p')
        updateresult = []

        for i in result:
            if "<strong>" in str(i):
                if '：' in i.text:
                    sname, stext = re.split('：', i.text)
                    for code, name in stocklist.values:
                        if sname == name:
                            updateresult.append([code, sname, datetime.datetime.strptime(stime[:10], '%m/%d/%Y'),
                                                 stext])
                else:
                    for code, name in stocklist.values:
                        if name in i.text:
                            updateresult.append([code, name, datetime.datetime.strptime(stime[:10], '%m/%d/%Y'),
                                                 i.text])

        df = pd.DataFrame(updateresult, columns=['code', 'name', 'time', 'text'])
        df['time'] = df['time'].astype('datetime64[ns]')

        for code in df['code'].values:
            duplicate = df[df['code'] == code].reset_index(drop=True)

            if len(df[df['code'] == code]) != 1:
                text = ''
                for i in range(len(duplicate) - 1):
                    if duplicate['text'][i][:8] == duplicate['text'][i + 1][:8]:
                        text = duplicate['text'][i]
                    else:
                        text = duplicate['text'][i] + duplicate['text'][i + 1]
                final.append([code, duplicate['name'][0], duplicate['time'][0], text])
            else:
                final.append([code, duplicate['name'][0], duplicate['time'][0], duplicate['text'][0]])
    final = pd.DataFrame(final, columns=['code', 'name', 'time', 'text'])

    sql_lastdate="select DISTINCT `date` from `indexdb` ORDER BY `date` DESC limit 1"
    sdate = pd.read_sql(sql_lastdate, engine)['date'][0]
    checkdatelist=set(final['time'].values)
    for checkdate in checkdatelist:
        sql_check="select DISTINCT `focus` from `usefuldata` WHERE `date` = '%s'"%(str(checkdate))
        scheck = pd.read_sql(sql_check,engine)['focus']

        if len(scheck)<=1:
            df = final[final['time']==checkdate].reset_index(drop=True).values
            for scode,sname,stime,stext in df:
                stime = datetime.date(int(str(stime)[0:4]),int(str(stime)[5:7]),int(str(stime)[8:10]))
                if stime>sdate:
                    stime=sdate
                else:
                    stime=stime
                params = (scode, str(stime), stext, stext)
                # print(params)
                sql = "insert into `usefuldata` (`code`,`date`,`focus`) VALUE (%s,%s,%s) ON DUPLICATE KEY UPDATE `focus` = %s;"
                try:

                    engine.execute(sql,params)
                except Exception as e:
                    print("local:",e)
                    print(scode,sname,str(stime),stext)


if __name__ == '__main__':
    update_focussql()
