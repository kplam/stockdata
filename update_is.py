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
import re,datetime

def get_is_data(date,code):
      url="http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=CCJGMX&p=1&ps=5000&fd=%s&code=%s&js=[(x)]"%(date,code)
      html=myspyder(url,proxy=0)
      try:
         doc = html.content.decode('utf-8')
         if doc != '[{stats:false}]':
             doc = eval(doc)
             table = []
             for data in doc:
                table.append(re.split(',',data))
             df = pd.DataFrame(table,columns=['code','stockname','fundcode','fundname','type','vol','amo','percent','percent_cir','date'])
             df = df[['code','date','fundcode','fundname','type','vol','amo','percent','percent_cir']]
             return True,df
         else:
             return True,pd.DataFrame()
      except Exception as e:
         print("%s,%s:%s"%(code,date,e))
         return False,pd.DataFrame()

def cal_datelist(type='all'):
    if type == 'all':
        datelist = []
        Q1,Q2,Q3,Q4 = '03-31','06-30','09-30','12-31'
        yearlist = ['2012','2013','2014','2015','2016','2017']
        for year in yearlist:
          datelist.append(year + '-' + Q1)
          datelist.append(year + '-' + Q2)
          datelist.append(year + '-' + Q3)
          datelist.append(year + '-' + Q4)
        return datelist
    if type == 'single':
        today = datetime.date.today()
        if today <= datetime.date(int(str(today)[:4]),3,31):
            return [str(int(str(today)[:4])-1)+'-12-31']
        elif datetime.date(int(str(today)[:4]),3,31) < today <= datetime.date(int(str(today)[:4]),4,30):
            return [str(datetime.date(int(str(today)[:4]),3,31)),str(int(str(today)[:4])-1)+'-12-31']
        elif datetime.date(int(str(today)[:4]),4,30) < today <= datetime.date(int(str(today)[:4]),6,30):
            return [str(datetime.date(int(str(today)[:4]),3,31))]
        elif datetime.date(int(str(today)[:4]),6,30) < today <= datetime.date(int(str(today)[:4]),9,30):
            return [str(datetime.date(int(str(today)[:4]),6,30))]
        elif datetime.date(int(str(today)[:4]),9,30) < today <= datetime.date(int(str(today)[:4]),12,31):
            return [str(datetime.date(int(str(today)[:4]),9,30))]

def get_all_is_date(datelist=cal_datelist(type='single')):
   sql_query = "INSERT IGNORE INTO `institutional`(`code`, `date`, `fundcode`, `fundname`, `type`, `vol`, `amo`, `percent`, `percent_cir`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
   stocklist = get_stocklist()
   errorlist=[]
   engine=conn()
   for code in stocklist:
      # if code[0] == '6' and  int(code)>600500:
      print(code)

      for date in datelist:
         b,data = get_is_data(date,code)
         if b == False:
            errorlist.append([date,code])
         else:
            for param in data.values:
               params = [str(ele) for ele in param]
            engine.execute(sql_query,params)

   return errorlist

def errorretry(errorlist):
    list = []
    sql_query = "INSERT IGNORE INTO `institutional`(`code`, `date`, `fundcode`, `fundname`, `type`, `vol`, `amo`, `percent`, `percent_cir`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    engine = conn()

    for date, code in errorlist:
        try:
            b,data = get_is_data(date, code)
            if b == False:
                errorlist.append([date, code])
            else:
                for param in data.values:
                    params = [str(ele) for ele in param]
                    engine.execute(sql_query, params)
        except:
            list.append([date, code])

    return list


if __name__ == '__main__':

   errorlist=get_all_is_date(datelist=cal_datelist(type='single'))
   times_retry=3
   print(errorlist)
   while len(errorlist)>0 and times_retry !=0:
        errorlist=errorretry(errorlist)
        times_retry -=1
   # b,df=get_is_data('2017-12-31','000005')
   # print(df)


