#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""

from kpfunc.getdata import *
import requests as rqs
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from random import random
import re,time,datetime
import pandas as pd


def myspyder(url):
    s = rqs.session()
    s.mount('http://', HTTPAdapter(pool_connections=3, pool_maxsize=3, max_retries=10, pool_block=False))
    s.mount('https://', HTTPAdapter(pool_connections=3, pool_maxsize=3, max_retries=10, pool_block=False))
    rqs_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, compress',
                  'Cache-Control': 'max-age=0',
                  'Cookie':'__jsluid=6929a630bc56ed6c957b26af2da5729a; CNZZDATA1261728527=291603669-1495773261-%7C1509435159; tb_history=jPSj5I; live_guest=98d3659ccec522f5; 55188_passport=%2BEtAnhGfdq0YX4McS9TuKNzz923SZobv%2FjGYxG5ZR7xU%2Bp02RUCByk%2BDT1U%2F2n%2BqUPATmbE1sT8VQByxIV3%2Bk39apPI4eEq%2BWY2ls7IxULuWcKDccjYWVuSWMKWvB3GUEv5CPtgbgLTsVu50g2bm4a0Rt0mARnn1yXaIm6JqyOs%3D; cdb2_auth=23yq1zfEU4FHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Iu%2BD; cdb2_auth=iSj81GKfVYBHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Ig; 55188_live_auth=2wIqAz2xvEPDKorJ2%2FQVNCBf8LvY2Y5j%2Bi4GFO4PDT9Gr%2FsYR51yMQR0zkP5k1zAiOgML5eXxZNFBtAKgO6mMOIbvjZE1qCABWhuhg0ap%2FnMqxZc4K%2FdlUAwM0Lr4Eh69Mr3T2cuzMC4%2BE%2FLUcJihEf98%2BrOjlWjXaX7wxJpwIg%3D; cdb2_sid=Xq52uq; cdb2_onlineusernum=880230; Hm_lvt_0233b908b2bf29bfd788abd7ee3556da=1517791725,1517835514,1517923153,1518187882; Hm_lpvt_0233b908b2bf29bfd788abd7ee3556da=1518188068',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                '/53.0.2785.104 Safari/537.36 Core/1.53.4033.400 QQBrowser/9.6.12624.400'}
    try:
        # if len(proxies) != 0:
        #     rqs_url = s.get(url, headers=rqs_header, timeout=10, proxies=proxies)
        # else:
        rqs_url = s.get(url, allow_redirects=True, headers=rqs_header, timeout=10)
        rqs_url.raise_for_status()
    except rqs.RequestException as e:
        rqs_url = "error!"
    s.close()
    return rqs_url

def get_urllist_one():
    links = []
    try:
        url = "http://www.55188.com/forumdisplay.php?fid=8&filter=type&typeid=138&page=4"
        html = myspyder(url)
        doc = bs(html.content, 'html5lib')
        subject = doc.select('tbody')
        # print(subject)
        for ele in subject:
            aherf = ele.select('a')
            for elem in aherf:
                if '上证早知道' in elem.text or '时报财富资讯' in elem.text or '中证快报' in elem.text or '中证投资参考' in elem.text:
                    link = elem.get('href')
                    if re.match('thread-\d*-\d*-\d*.html',link):
                        link = "http://www.55188.com/"+link
                        links.append(link)
    #     # print(subject)
    #     for i in range(len(subject.select('.center_subject'))):
    #         post = subject.select('.center_lastpost')[i]
    #         etime = post.find_all('a')[1].text
    #         etime = datetime.datetime.strptime(etime, "%Y-%m-%d %H:%M")
    #         if etime > datetime.datetime.today() - datetime.timedelta(days=2):
    #             # print(etime, subject.select('.center_subject')[i].text)
    #
    #             link = "http://www.55188.com/" + str(subject.select('.center_subject')[i].a.get('href'))
    #             links.append(link)
        links = list(set(links))
    except Exception as e:
        print(e)
    return links

def get_zzd(links=get_urllist_one(),check=1,ser='both'):
    source = '55188.com'
    stype = '【早知道】'
    # print(links)
    engine = conn()
    if check ==1:
        checkdate = datetime.date.today() - datetime.timedelta(days=7)
        sql_check = "select `link` from `news` WHERE `type`='【早知道】' and `datetime` >='%s'" % (checkdate)

        urlchecklistlocal = pd.read_sql(sql_check, engine)['link'].values


    for link in links:
        if check ==1:

            if link not in urlchecklistlocal :#or link not in urlchecklistserver:
                    # print(link)
                    try:
                        htmldetail = myspyder(link)
                        soupdetail = bs(htmldetail.content,'html5lib')

                        title = soupdetail.select("tbody > tr:nth-of-type(1) > td.postcontent > div.postmessage > div.post_subject > h2")[0].text
                        title = title.replace(' ','')
                        stime = soupdetail.select("tbody > tr:nth-of-type(1) > td.postcontent > div.postinfo")[0].text
                        stime = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",stime)[0]
                        stime = datetime.datetime.strptime(stime,'%Y-%m-%d %H:%M')

                        content = str(soupdetail.select("#firstpostcontent")[0])
                        content=content.replace('<font color="#EFEFEF">股票论坛 www.55188.com</font>','')

                        param= (source,stype,title,link,content,stime)
                        print(title, stime, "\n", link)
                        sql = "INSERT IGNORE INTO `news`(`source`, `type`, `title`, `link`, `content`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s)"
                        if stime>datetime.datetime.today()-datetime.timedelta(days=2):

                            try:
                                engine.execute(sql,param)

                            except Exception as e:
                                print(e)

                    except Exception as e:
                        print(e)

        else:
            try:
                htmldetail = myspyder(link)
                soupdetail = bs(htmldetail.content, 'html5lib')

                title = soupdetail.select(
                    "tbody > tr:nth-of-type(1) > td.postcontent > div.postmessage > div.post_subject > h2")[0].text
                title = title.replace(' ', '')

                stime = soupdetail.select("tbody > tr:nth-of-type(1) > td.postcontent > div.postinfo")[0].text
                stime = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", stime)[0]
                stime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M')

                content = str(soupdetail.select("#firstpostcontent")[0])
                content = content.replace('<font color="#EFEFEF">股票论坛 www.55188.com</font>', '')

                param = (source, stype, title, link, content, stime)
                print(title, stime,"\n",link)
                sql = "INSERT IGNORE INTO `news`(`source`, `type`, `title`, `link`, `content`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s)"
                if stime > datetime.datetime.today()-datetime.timedelta(days=2):
                    try:
                        engine.execute(sql, param)
                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)
        time.sleep(random()*10+0.3)


if __name__ == '__main__':
    get_zzd(links=get_urllist_one(),check=1)


