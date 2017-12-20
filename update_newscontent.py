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
from kpfunc.spyder import myspyder
from kpfunc.function import path
import time,datetime,re,random,json
"""
http://app.stcn.com/?app=article&controller=article&action=fulltext&contentid=
"""
def news_content():
    # ===================
    conn=localconn()
    today=datetime.date.today()
    # ===================set requests================== #
    rqs = rq.session()
    rqs.keep_alive = False
    rqshead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
    # ===================get news content================ #

    sql_news_null = "SELECT * FROM `news` WHERE `content` IS NULL OR (`title` LIKE '%%更新中%%' and `datetime`>='%s')"%(today)
    df_listurl = pd.read_sql(sql_news_null,conn)
    list_url = df_listurl['link'].values
    list_title = df_listurl['title'].values

    list_content = df_listurl['content'].values
    errorlist = []
    # list_url=['http://kuaixun.stcn.com/2017/1110/13761584.shtml']
    #ip_list =pd.read_csv('ip.csv')['ip'].values


    for i in range(len(list_url)):
        time.sleep(random.random()/10+3)
        newsid= re.split("\.", re.split("\/", list_url[i])[-1])[0]
        newurl="http://app.stcn.com/?app=article&controller=article&action=fulltext&contentid=%s"%(newsid)
        try:
            html = myspyder(newurl,proxy=0).content.decode('utf-8')[1:-2]
            newscontent = json.loads(html)['content']
            # print(newscontent)
            # newsSoup = bs(html, 'html.parser')
            # newsSouptitle = newsSoup.select(".intal_tit")[0].h2.text
            # newsSoup = newsSoup.select(".txt_con")[0]
            # [s.extract() for s in newsSoup('a')]
            # [s.extract() for s in newsSoup('script')]
            # [s.extract() for s in newsSoup('div')]
            # newscontent = str(newsSoup)
            newscontent = "".join(re.split("\|STCNTTTP\|.+\|STCNTTTP\|", newscontent))
            if newscontent == list_content[i]:
                pass
            else:
                print("NEW:",list_title[i])
                # print(newscontent)
                sql_update_newscontent ="update `news` set `content`=%s WHERE `link`=%s"
                param=(newscontent,list_url[i])
                cur=conn.cursor()
                cur.execute(sql_update_newscontent,param)
                conn.commit()
        except Exception as e:
            # print(url,e)
            errorlist.append((list_url[i],e))
    df_errorlist = pd.DataFrame(errorlist,columns=['link','error'])
    df_errorlist.to_csv(path()+'/error/update_newscontent.csv')
    conn.close()

if __name__ == '__main__':
    news_content()