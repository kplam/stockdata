#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
from kpfunc.getdata import localconn
from kpfunc.spyder import spyder
from kpfunc.function import path
import time,datetime
import random

def news_content():
    # ===================
    conn=localconn()
    today=datetime.date.today()
    # ===================set requests================== #
    rqs = rq.session()
    rqs.keep_alive = False
    rqshead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    # ===================get news content================ #

    sql_news_null = "SELECT * FROM `news` WHERE `content` IS NULL OR(`title` LIKE '%%更新中%%' and `datetime`>='%s')"%(today)
    df_listurl = pd.read_sql(sql_news_null,conn)
    list_url = df_listurl['link'].values
    errorlist = []
    # list_url=['http://kuaixun.stcn.com/2017/1110/13761584.shtml']
    #ip_list =pd.read_csv('ip.csv')['ip'].values


    for url in list_url:
        print(url)
        time.sleep(random.random()/10+3)
        try:
            html = spyder(url,proxy=0).content
            newsSoup = bs(html, 'html.parser')
            newsSouptitle = newsSoup.select(".intal_tit")[0].h2.text
            newsSoup = newsSoup.select(".txt_con")[0]
            [s.extract() for s in newsSoup('a')]
            [s.extract() for s in newsSoup('script')]
            [s.extract() for s in newsSoup('div')]
            newscontent = str(newsSoup)
            # print(newscontent)
            sql_update_newscontent ="update `news` set `content`='%s',`title`='%s'WHERE `link`='%s'"%(newscontent,newsSouptitle,url)
            cur=conn.cursor()
            cur.execute(sql_update_newscontent)
            conn.commit()
        except Exception as e:
            # print(url,e)
            errorlist.append((url,e))
    df_errorlist = pd.DataFrame(errorlist,columns=['link','error'])
    df_errorlist.to_csv(path()+'/error/update_newscontent.csv')

if __name__ == "__main__":
    news_content()