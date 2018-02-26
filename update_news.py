#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
from kpfunc.spyder import myspyder
from kpfunc.function import path
from random import random
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_news(url,proxy):
    source = 'stcn.com'
    html = "error!"
    times_retry = 3
    while html == "error!" and times_retry!=0:
        html = myspyder(url,proxy=proxy)
        times_retry = times_retry -1
    html = html.content
    # print(news.decode('utf-8'))
    newsSoup = bs(html, 'html.parser')
    newslist = newsSoup.select(".mainlist")
    newslist = bs(str(newslist[0]),'html.parser')
    newslist = newslist.find_all("p")
    result = []
    for i in range(len(newslist)):
        news=str(newslist[i])
        stype= bs(news,'html.parser').a.text
        title = bs(news,'html.parser').a.next_element.next_element.text
        link = bs(news,'html.parser').a.next_element.next_element.attrs['href']
        datetime = str(bs(news,'html.parser').span.text)[1:20]
        result.append((source,stype,title,link,datetime))

    result= pd.DataFrame(result,columns=['source','type','title','link','datetime'])
    result['datetime'] =result['datetime'].astype('datetime64[ns]')
    return result

def stcn_news(ser='both'):
    """
    :param ser: local/server/both
    :return:
    """
    import datetime
    # ===================
    lastday= datetime.date.today()-datetime.timedelta(days=2)
    if ser == 'local' or ser == 'both':
        conn = localconn()
    if ser == 'server' or ser == 'both':
        conns = serverconn()
    #读取最近两天地址，以减少写入次数
    sql_check ="select `link` from `news` where `datetime`>='%s'"%(lastday)
    linklist=pd.read_sql(sql_check,localconn())['link'].values
    # ================================================= #
    pages =range(1,2)
    url= "http://kuaixun.stcn.com/index_%s.shtml"
    source ='stcn.com'
    urllist = [url%(page_id) for page_id in pages]
    newsresult = pd.DataFrame()
    errorlist=[]
    for i in range(len(urllist)):
        try:
            result = get_news(urllist[i],proxy=0)
            newsresult = pd.concat((result,newsresult),ignore_index=True)
            sleep(random()/10+1)
        except Exception as e:
            print(e)
            errorlist.append(e)

    for j in range(len(newsresult)):
        try:
            stype=newsresult.get_value(j,'type')
            title=newsresult.get_value(j,'title')
            link = newsresult.get_value(j,'link')
            datetime =newsresult.get_value(j,'datetime')
            if link not in linklist:
                sql_update= "insert ignore INTO `news`(`source`, `type`, `title`, `link`, `datetime`) VALUES (%s,%s,%s,%s,%s)"
                param=(source,stype,title,link,str(datetime))
                if ser == 'local' or ser =='both':
                    cur = conn.cursor()
                    cur.execute(sql_update,param)
                    conn.commit()
                if ser =='server' or ser == 'both':
                    curs = conns.cursor()
                    curs.execute(sql_update,param)
                    conns.commit()
            else:
                pass
        except Exception as e:
            print(e)
            errorlist.append(e)
    dfErrorList = pd.DataFrame(errorlist)
    dfErrorList.to_csv(path()+'/error/update_news.csv')

if __name__ == '__main__':
    stcn_news(ser='local')
