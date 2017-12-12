# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
from kpfunc.spyder import spyder
from kpfunc.getdata import *
from kpfunc.function import path
from time import sleep
from random import random
import datetime,re


class update_bar:
    def __init__(self,conn=localconn()):
        self.conn =conn
        self.stocklist = get_stocklist_prefix('sh','sz',pre=1)
        self.indexlist = get_indexlist_prefix('sh','sz',pre=1)
        self.url = "http://hq.sinajs.cn/list=%s"
        self.urllist = []
        self.htmllist = []

    def get_urllist(self,list='index'):
        inputlist = self.indexlist if list=='index' else self.stocklist
        param = ''
        for i in range(len(inputlist)):
            param = param + inputlist[i] + ','
            if (i + 1) % 200 == 0 or i == len(inputlist) - 1:
                self.urllist.append(self.url % (param))
                param = ''
        return self.urllist

    def get_data(self,proxy=0):
        for url in self.urllist:
            try:
                html = "error!"
                times_retry= 3
                while html=="error!" and times_retry != 0:
                    html = spyder(url,proxy=proxy)
                    times_retry -=1
            except:
                pass
            html = html.content.decode('gbk')
            html = html.replace("\n", "")
            html = re.split("\;", html)
            self.htmllist = self.htmllist + html
        return self.htmllist

    def to_df(self):
        table =[]
        for html in self.htmllist:
            try:
                code = html[13:19]
                data = re.findall("\"(.*?)\"",html)
                data = re.split(",",data[0])
                data =[code]+data
                table.append(data)
            except:
                pass
        dayline = pd.DataFrame(table,columns=['code','name','open','preclose','close','high','low','e','f','vol','amo','g','h','I','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','date','aa','ab'])
        dayline = dayline[['code','date','high','open','low','close','vol','amo']]
        dayline['date'] = dayline['date'].astype('datetime64')
        dayline['close'] = dayline['close'].astype('float32')
        dayline['high'] = dayline['high'].astype('float32')
        dayline['low'] = dayline['low'].astype('float32')
        dayline['open'] = dayline['open'].astype('float32')
        dayline['vol'] = dayline['vol'].astype('float32')
        dayline['amo'] = dayline['amo'].astype('float32')
        dayline = dayline[dayline['vol']>0]
        return dayline

    def update_index(self):
        self.urllist = []
        self.htmllist = []
        self.get_urllist('index')
        self.get_data(proxy=0)
        df_index = self.to_df()
        try:
            df_index.to_sql('indexdb',self.conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
        except Exception as e:
            print(e)
        return df_index

    def update_stock(self):
        self.urllist = []
        self.htmllist = []
        self.get_urllist('stock')
        self.get_data(proxy=0)
        df_stock = self.to_df()
        try:
            df_stock.to_sql('indexdb',self.conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
        except Exception as e:
            print(e)
        return df_stock

    def update_stock_status(self):    #  update stock status
        stocklist = update_bar().stocklist
        sql_index = "select * from `indexdb` WHERE `code`='000001' order by `date` desc limit 0,1"
        df_index = pd.read_sql(sql_index,self.conn)
        date_index = df_index.get_value(0,'date')
        print("Updating stock status...")
        for code in stocklist:
            sql_daybar = "select * from `dayline` where `code`='%s'order by `date` desc limit 0,1" % (code[2:])
            df_daybar = pd.read_sql(sql_daybar,self.conn)
            if df_daybar.empty == False:
                date_daybar = df_daybar.get_value(0,'date')
                if date_daybar == date_index:
                    sql_stocklist = "update `stocklist` set `交易状态`=1 where 证券代码='%s'" % (code)
                elif date_index > date_daybar:
                    sql_stocklist = "update `stocklist` set `交易状态`=0 where 证券代码='%s'" % (code)
                else:
                    sql_stocklist = "update `stocklist` set `交易状态`=9 where 证券代码='%s'" % (code)
            else:
                sql_stocklist = "update `stocklist` set `交易状态`=9 where 证券代码='%s'" % (code)
            cur = self.conn.cursor()
            cur.execute(sql_stocklist)
            self.conn.commit()

if __name__ == '__main__' :
    update_bar().update_stock()
    print("Update stock daybar done!")
    update_bar().update_index()
    print("Update index daybar done!")
    update_bar().update_stock_status()
    print('Update Stock Status Done!')
