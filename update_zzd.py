#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""

from kpfunc.getdata import localconn,serverconn
import requests as rqs
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from random import random
import re,time,datetime
import pandas as pd


"""
http://www.55188.com/search.php?searchid=88&orderby=dateline&ascdesc=desc&searchsubmit=yes
http://www.55188.com/search.php?searchid=88&orderby=dateline&ascdesc=desc&searchsubmit=yes&page=2
http://www.55188.com/viewthread.php?tid=8265824&page=1&authorid=353347

"""

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

# def get_urllist_all():
#     links=[]
#     for num in range(1,425):
#         print(num)
#         try:
#             url = "http://www.55188.com/search.php?searchid=88&orderby=dateline&ascdesc=desc&searchsubmit=yes&page=%s"%(num)
#             html = myspyder(url)
#             soup = bs(html.content,'html5lib')
#             soup = soup.select('table')[0]
#             for link in soup.find_all('a'):
#                 if re.match(u"http://www.55188.com/viewthread.php\?tid=\d*",link.get('href')):
#                     links.append(link.get('href'))
#         except Exception as e:
#             print(e)
#         time.sleep(random()/10+0.3)
#     links = list(set(links))
#     return links

def get_urllist_one():
    links = []
    try:
        url = "http://www.55188.com/space-uid-353347.html"
        html = myspyder(url)
        doc = bs(html.content, 'html5lib')
        subject = doc.select('#module_mythreads')[0]
        # print(subject)
        for i in range(len(subject.select('.center_subject'))):
            post = subject.select('.center_lastpost')[i]
            etime = post.find_all('a')[1].text
            etime = datetime.datetime.strptime(etime, "%Y-%m-%d %H:%M")
            if etime > datetime.datetime.today() - datetime.timedelta(days=2):
                # print(etime, subject.select('.center_subject')[i].text)

                link = "http://www.55188.com/" + str(subject.select('.center_subject')[i].a.get('href'))
                links.append(link)
        links = list(set(links))
    except Exception as e:
        print(e)
    return links


def get_zzd(links=get_urllist_one(),check=1,ser='both'):
    source = '55188.com'
    stype = '【早知道】'
    # print(links)
    if check ==1:
        checkdate = datetime.date.today() - datetime.timedelta(days=7)
        sql_check = "select `link` from `news` WHERE `type`='【早知道】' and `datetime` >='%s'" % (checkdate)
        urlchecklistlocal = pd.read_sql(sql_check, localconn())['link'].values
        urlchecklistserver = pd.read_sql(sql_check, serverconn())['link'].values


    for link in links:
        if check ==1:
            if link not in urlchecklistlocal or link not in urlchecklistserver:
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
                        if ser=='both' or ser =='local':
                            try:
                                conn = localconn()
                                cur = conn.cursor()
                                cur.execute(sql,param)
                                conn.commit()
                                conn.close()
                            except Exception as e:
                                print(e)
                        if ser == 'both' or ser == 'server':
                            try:
                                conns = serverconn()
                                curs = conns.cursor()
                                curs.execute(sql,param)
                                conns.commit()
                                conns.close()
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

                    if ser == 'both' or ser == 'local':
                        try:
                            conn = localconn()
                            cur = conn.cursor()
                            cur.execute(sql, param)
                            conn.commit()
                            conn.close()
                        except Exception as e:
                            print(e)
                    if ser == 'both' or ser == 'server':
                        try:
                            conns = serverconn()
                            curs = conns.cursor()
                            curs.execute(sql, param)
                            conns.commit()
                            conns.close()
                        except Exception as e:
                            print(e)
            except Exception as e:
                print(e)
        time.sleep(random()*10+0.3)


if __name__ == '__main__':
    get_zzd()