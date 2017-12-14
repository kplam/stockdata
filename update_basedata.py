#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn,get_df_stocklist
from bs4 import BeautifulSoup as bs
from kpfunc.spyder import myspyder
from kpfunc.function import txt_pre,path
from time import sleep
from random import random
import pandas as pd
"""

http://data.eastmoney.com/gstc/search.ashx?SortType=SECURITYCODE&SortRule=1&PageIndex=1&PageSize=5000&jsObj=pyMzRbUF&marketValue=&keyWord=&peRation=&pbRation=&mainPoint=Qbtc&rt=50417793

主营分析：http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code=sh603533
"""
def update_embasedata(stocklist,ser,proxy):
    Errorlist=[]
    if ser == "server":
        conn = serverconn()
    elif ser =="local":
        conn = localconn()
    for i in range(len(stocklist)):
        sqli = "UPDATE  `basedata` SET  `证券代码` = %s,  `证券简称` = %s,  `公司名称` = %s,  `英文名称` = %s, " \
               " `曾用名` = %s,  `公司简介` = %s,  `成立日期` = %s,  `工商登记号` = %s,  `注册资本` = %s,  `法人代表` = %s, " \
               " `所属证监会行业` = %s,  `员工总数` = %s,  `总经理` = %s,  `董事会秘书` = %s,  `省份` = %s,  `城市` = %s,  " \
               "`注册地址` = %s,  `办公地址` = %s,  `邮编` = %s,  `电话` = %s,  `传真` = %s,  `电子邮件` = %s,  " \
               "`公司网站` = %s,  `审计机构` = %s,  `法律顾问` = %s,  `经营分析` = %s,  `简史` = %s,  `核心题材` = %s " \
               "WHERE `basedata`.`证券代码` = %s"
        symbol = stocklist.get_value(i, '证券代码') + "01" if stocklist.get_value(i, '证券代码')[
                                                              0] == "6" else stocklist.get_value(i, '证券代码') + "02"
        sName = stocklist.get_value(i, '证券简称')
        try:
            Intr = myspyder('http://soft-f9.eastmoney.com/soft/gp3.php?code=%s' % (symbol),proxy=proxy).content
            Conc = myspyder('http://soft-f9.eastmoney.com/soft/gp30.php?code=%s' % (symbol),proxy=proxy).content
            IntrSoup = bs(Intr, 'html5lib')
            ConcSoup = bs(Conc, 'html5lib')
            stockdata = []
            stockdata.append(symbol)
            stockdata.append(sName)
            for tr in IntrSoup.find_all(width=880):
                stockdata.append(txt_pre(tr.text.strip()))
            point = ConcSoup.p
            del point['style']
            stockdata.append(str(point))
            stockdata.append(symbol)
            print("BaseData:",symbol[:-2], sName, round(i / (len(stocklist))*100,2))
            cur = conn.cursor()
            cur.execute(sqli, tuple(stockdata))
            conn.commit()
            sleep((random() / 10 + 1))
        except Exception as e:
            print(symbol[:-2],sName,e)
            Errorlist.append((symbol[:-2],sName,e))
    conn.close()
    Errorlist = pd.DataFrame(Errorlist,columns=['证券代码','证券简称','error'])
    Errorlist.to_csv(path()+'/error/update_basedata.csv')
    return Errorlist
if __name__ == "__main__" :
    # stocklist = get_df_stocklist()
    sql = "SELECT `证券代码`,`证券简称` FROM `basedata` WHERE `公司名称` IS NULL or `核心题材`='<p>该品种暂无此项记录!</p>'"
    stocklist = pd.read_sql(sql,localconn())
    times_retry = 10
    while len(stocklist) > 0 and times_retry != 0:
        stocklist = update_embasedata(stocklist, "local", 0)
        times_retry -= 1