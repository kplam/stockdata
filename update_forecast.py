#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-01
@author: kplam
"""
import datetime,re
import pandas as pd
from kpfunc.getdata import localconn,serverconn,get_stocklist
from kpfunc.spyder import myspyder
from kpfunc.function import path

def get_forecast(conn=localconn(),proxy=0,lastday=0,update=1):
    """
    :param conn: 选择更新的数据库，localconn/serverconn
    :param proxy: 设置是否使用ip代理，0为不开启，1为开启
    :param lastday: 上次更新距离今天多长时间，默认当天为0
    :param update: 设置更新还是重建，更新设为1，其他为重建
    :return:
    """
    errorList=[]
    today = datetime.date.today()-datetime.timedelta(days=lastday)
    print("FORECAST:",today)
    iyear =int(str(today)[0:4])
    imonth= int(str(today)[5:7])
    List_stock = get_stocklist()
    iLong = int((round(len(List_stock) / 1000, 0) + 1) * 1000)
    Q4 = datetime.datetime(iyear-1,12,31).strftime('%Y-%m-%d') if imonth <=2 else \
        datetime.datetime(iyear,12,31).strftime('%Y-%m-%d')
    Q3 = datetime.datetime(iyear-1,9,30).strftime('%Y-%m-%d') if imonth < 8 else \
        datetime.datetime(iyear,9,30).strftime('%Y-%m-%d')
    Q2 = datetime.datetime(iyear-1,6,30).strftime('%Y-%m-%d') if imonth < 5 else \
        datetime.datetime(iyear, 6, 30).strftime('%Y-%m-%d')
    Q1 = datetime.datetime(iyear, 3, 31).strftime('%Y-%m-%d')
    List_Quarter =[Q1,Q2,Q3,Q4]
    df_forecast = pd.DataFrame()
    for Quarter in List_Quarter:
        url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJYG&fd=%s&st=4&sr=true&p=1&ps=%s' \
              % (Quarter, iLong)
        content = "error!"
        times_retry = 3
        while content =="error!" and times_retry!=0:
            content = myspyder(url,proxy=proxy).content.decode('utf-8')
            times_retry -= 1
        print("FORECAST:",Quarter,"数据抓取完毕，正在对数据进行处理...")
        try:
            return_list = re.findall("\"(.*?)\"", content)
            fctable = []
            for j in range(len(return_list)):
                appd = re.split("\,", return_list[j])
                fctable.append(appd)
            fctable = pd.DataFrame(fctable,
                                   columns=['code', '股票简称', '业绩变动', '变动幅度', '预告类型', '同期净利润'
                                       , '预喜预悲', 'date','财报日期'])
            fctable = fctable[['code', '业绩变动', '变动幅度', '预告类型', '同期净利润', 'date', '财报日期']]
            df_forecast = pd.concat((df_forecast, fctable)).sort_values('date', ascending=False).drop_duplicates()
        except Exception as e:
            errorList.append(e)
    df_forecast['date'] = df_forecast['date'].astype('datetime64', error='ignore')
    df_forecast['财报日期'] = df_forecast['财报日期'].astype('datetime64', error='ignore')
    print("FORECAST: 数据处理完毕，正在更新数据库...")
    if update == 1:
        df_forecast = df_forecast[df_forecast['date']>=today]
    else:
        df_forecast = df_forecast
    for j in range(len(df_forecast)):
        try:
            Scode = df_forecast.get_value(j,'code')
            Sdate = str(df_forecast.get_value(j,'date'))
            Schange = df_forecast.get_value(j, '业绩变动')
            Spercent = df_forecast.get_value(j, '变动幅度')
            Stype = df_forecast.get_value(j, '预告类型')
            Sprofit = df_forecast.get_value(j, '同期净利润')
            Srepdate = df_forecast.get_value(j, '财报日期')
            ul = re.split("～", Spercent)
            if len(ul) == 2:
                upper = ul[1].replace('%', '')
                lower = ul[0].replace('%', '')
            elif len(ul) == 1 and ul[0] != '':
                upper = ul[0].replace('%', '')
                lower = None
            else:
                upper = None
                lower = None

            sql_update = "INSERT IGNORE INTO `forecast`(`code`, `date`, `业绩变动`, `变动幅度`, `预告类型`, `同" \
                         "期净利润`, `财报日期`,`上限`,`下限`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            param = (Scode, Sdate, Schange, Spercent, Stype, Sprofit, Srepdate, upper, lower)
            cur = conn.cursor()
            cur.execute(sql_update,param)
            conn.commit()
        except Exception as e:
            errorList.append(e)
    dfErrorList = pd.DataFrame({'error': errorList})
    dfErrorList.to_csv(path() + '/error/update_forecast.csv')
    print("FORECAST: 更新数据库完毕!")
    return dfErrorList

if __name__=="__main__":
    get_forecast()