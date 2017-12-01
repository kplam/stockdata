#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22

@author: kplam
"""
from kpfunc.getdata import get_stocklist_prefix,localconn
from random import random
import time
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
import numpy as np


def get_shareholder_data(stocklist):
    conn = localconn()
    errorlist=[]
    rqs = rq.session()
    rqs.keep_alive = False
    rqs_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    for code in stocklist:
        try:
            print(code[0:6])
            rqs_url = "http://soft-f9.eastmoney.com/soft/gp51.php?code=%s&exp=1" % (code)
            html = rq.get(rqs_url,headers=rqs_header,timeout=10)
            with open("./data/cirholder/"+code[0:6]+".xls","wb") as f51:
                f51.write(html.content)
            f51.close()
            with open("./data/cirholder/"+code[0:6]+".xls", "rb") as f510:
                soup = bs(f510.read(), 'html.parser')
                list = soup.select('data')
                list = [data.text for data in list]
                list = np.array(list).reshape(int(len(list) / 8), 8)
                df_gp51 = pd.DataFrame(list[1:],
                                       columns=['date', 'rank', 'name', 'type', 'quantity', 'percentage', 'change',
                                                'abh'], )
                df_gp51['code'] = code[0:6]
                df_gp51 = df_gp51[['code','date','rank', 'name', 'type', 'quantity', 'percentage', 'change',
                                                'abh']]
                newdata_51 = []
                for i in range(len(df_gp51)):
                    code = df_gp51.get_value(i, 'code')
                    date = df_gp51.get_value(i, 'date')
                    rank = df_gp51.get_value(i, 'rank')
                    name = df_gp51.get_value(i, 'name')
                    type = df_gp51.get_value(i, 'type')
                    quantity = df_gp51.get_value(i, 'quantity')
                    percentage = df_gp51.get_value(i, 'percentage')
                    if percentage =="--":
                        percentage = '0'
                    else:
                        percentage = percentage
                    change = df_gp51.get_value(i, 'change')
                    abh = df_gp51.get_value(i, 'abh')
                    quantity = float(quantity.replace(",", ""))
                    if change == "不变":
                        change = '0'
                    elif change == "新进":
                        change = quantity
                    else:
                        change = change
                    newdata_51.append([code, date, rank, name, type, quantity, percentage, change, abh])
                newdata_51 = pd.DataFrame(newdata_51,
                                       columns=['code', 'date', 'rank', 'name', 'type', 'quantity', 'percentage',
                                                'change', 'abh'])
                newdata_51['quantity'] = newdata_51['quantity'].astype('str')
                for j in range(len(newdata_51)):
                    sql_gp51 = "INSERT IGNORE INTO `cirholder`(`code`, `date`, `rank`, `name`, `type`, `quantity`, `percentage`," \
                               " `change`, `abh`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    sql_gp51_param = tuple(newdata_51.iloc[j].values)
                    cur = conn.cursor()
                    cur.execute(sql_gp51,sql_gp51_param)
                    conn.commit()
            f510.close()

            rqs_url2 = "http://soft-f9.eastmoney.com/soft/gp50.php?code=%s&exp=1" % (code)
            html2 = rq.get(rqs_url2,headers=rqs_header,timeout=10)
            with open("./data/shareholder/"+code[0:6]+".xls","wb") as f50:
                f50.write(html2.content)
            f50.close()
            with open("./data/shareholder/"+code[0:6]+".xls", "rb") as f500:
                soup = bs(f500.read(), 'html.parser')
                list = soup.select('data')
                list = [data.text for data in list]
                list = np.array(list).reshape(int(len(list) / 7), 7)
                df_gp50 = pd.DataFrame(list[1:],
                                       columns=['date', 'rank', 'name', 'quantity', 'percentage', 'change', 'type'], )
                df_gp50['code'] = code[0:6]
                df_gp50 = df_gp50[['code','date', 'rank', 'name', 'quantity', 'percentage', 'change', 'type']]
                newdata_50 = []
                for k in range(len(df_gp50)):
                    code = df_gp50.get_value(k, 'code')
                    date = df_gp50.get_value(k, 'date')

                    rank = df_gp50.get_value(k, 'rank')
                    name = df_gp50.get_value(k, 'name')
                    quantity = df_gp50.get_value(k, 'quantity')
                    percentage = df_gp50.get_value(k, 'percentage')
                    if percentage =="--":
                        percentage = '0'
                    else:
                        percentage = percentage
                    change = df_gp50.get_value(k, 'change')
                    type = df_gp50.get_value(k,'type')
                    quantity = float(quantity.replace(",", ""))
                    if change == "不变":
                        change = '0'
                    elif change == "新进":
                        change = quantity
                    else:
                        change = change
                    newdata_50.append([code, date, rank, name, quantity, percentage, change, type])
                newdata_50 = pd.DataFrame(newdata_50,
                                       columns=['code', 'date', 'rank', 'name', 'quantity', 'percentage',
                                                'change', 'type'])
                newdata_50['quantity'] = newdata_50['quantity'].astype('str')
                for l in range(len(newdata_50)):
                    sql_gp50 = "INSERT IGNORE INTO `shareholder`(`code`, `date`, `rank`, `name`, `quantity`, `percentage`," \
                               " `change`, `type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    sql_gp50_param = tuple(newdata_50.iloc[l].values)
                    cur = conn.cursor()
                    cur.execute(sql_gp50,sql_gp50_param)
                    conn.commit()
            f500.close()
            time.sleep(random()/10+1)
        except Exception as e:
            errorlist.append(code)
            print(code[0:6],e)
    return errorlist

stocklist = get_stocklist_prefix("01","02",0)
times_retry = 3
while len(stocklist) != 0 and times_retry != 0:
    stocklist = get_shareholder_data(stocklist)
    times_retry = times_retry - 1