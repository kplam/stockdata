#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22

@author: kplam
"""

"""
http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=CCJGMX&p=1&ps=5000&fd=2017-12-31&code=002411
"""

from kpfunc.spyder import myspyder
from kpfunc.getdata import *
import pandas as pd
import re

def get_is_data(date,code):
      url="http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=CCJGMX&p=1&ps=5000&fd=%s&code=%s&js=[(x)]"%(date,code)
      html=myspyder(url,proxy=0)
      # print(html.content)
      try:
         doc = html.content.decode('utf-8')
         doc = eval(doc)
         table = []
         for data in doc:
            table.append(re.split(',',data))
         df = pd.DataFrame(table,columns=['code','stockname','fundcode','fundname','type','vol','amo','percent','percent_cir','date'])
         df = df[['code','date','fundcode','fundname','type','vol','amo','percent','percent_cir']]
         return True,df
      except Exception as e:
         print("%s,%s:%s"%(code,date,e))
         return False,pd.DataFrame()

def cal_datelist():
   datelist = []
   Q1,Q2,Q3,Q4 = '3-31','06-30','09-30','12-31'
   yearlist = ['2012','2013','2014','2015','2016','2017']
   for year in yearlist:
      datelist.append(year + '-' + Q1)
      datelist.append(year + '-' + Q2)
      datelist.append(year + '-' + Q3)
      datelist.append(year + '-' + Q4)
   return datelist


def get_all_is_date(ser='both',datelist=cal_datelist()):
   sql_query = "INSERT IGNORE INTO `institutional`(`code`, `date`, `fundcode`, `fundname`, `type`, `vol`, `amo`, `percent`, `percent_cir`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
   stocklist = get_stocklist()
   errorlist=[]
   for code in stocklist:
      print(code)
      if ser == 'both' or ser == 'local':
         conn = localconn()
         cur = conn.cursor()
      if ser == 'both' or ser == 'server':
         conns = serverconn()
         curs = conns.cursor()
      for date in datelist:
         b,data = get_is_data(date,code)
         if b == False:
            errorlist.append([date,code])
         else:
            for param in data.values:
               params = [str(ele) for ele in param]
               if ser == 'both' or ser == 'local':
                  cur.execute(sql_query,params)
               if ser == 'both' or ser == 'server':
                  curs.execute(sql_query, params)
      if ser == 'both' or ser == 'local':
         conn.commit()
         conn.close()
      if ser == 'both' or ser == 'server':
         conns.commit()
         conns.close()
   return errorlist


if __name__ == '__main__':
   def retry(errorlist):
      list = []
      sql_query = "INSERT IGNORE INTO `institutional`(`code`, `date`, `fundcode`, `fundname`, `type`, `vol`, `amo`, `percent`, `percent_cir`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      conn = localconn()
      cur = conn.cursor()
      for date, code in errorlist:
         try:
            data = get_is_data(date, code)
            if data == False:
               errorlist.append([date, code])
            else:
               for param in data.values:
                  params = [str(ele) for ele in param]
                  cur.execute(sql_query, params)
               conn.commit()
         except:
            list.append([date, code])
      conn.close()
      return list


   errorlist=get_all_is_date(ser='local',datelist=cal_datelist())
   while len(errorlist)>0:
      errorlist=retry(errorlist)
   #
   # b,df=get_is_data('2012-3-31','000007')
   # print(df)


