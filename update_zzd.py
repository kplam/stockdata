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
                  # 'Cookie': '__jsluid=6929a630bc56ed6c957b26af2da5729a; CNZZDATA1261728527=291603669-1495773261-%7C1509435159; tb_history=jPSj5I; cdb2_oldtopics=D8265824D; cdb2_fid8=1517531268; live_guest=aaea041ea81c3ce7; cdb2_onlineusernum=880230; 55188_passport=9ONdxrpBaQXdm5bJmldyW5FlxidRvMBqAr4yIAEPqpE2gxZrwiXjZrr2pMwUIZJzKxpiUDVxAArpfhaM0bIVIV0TZmuoICVXTlBCJt8Vwg1t0n%2Fs03UlkW98jxCmFh7rAzHcFxrAgMlYqHym64LCa58VKIo03QxlO9imPGSBiw8%3D; cdb2_auth=23yq1zfEU4FHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Iu%2BD; cdb2_auth=iSj81GKfVYBHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Ig; 55188_live_auth=%2Bk62eHaAzpL1S9cCt2328eky56F6xHhgISWBABplU%2Bp5cbfGJnmHjGtFbhjVtcd58vSnUxgfgP%2FWNnMKstiQyNqIuNrjFq%2FYmHxFSMihqfTxgEboKd9p9tA0Mxvidv8dpb%2FWwOUe5w15c3JMsPNAcu9szA3Cr35doDO7FSL9l2E%3D; cdb2_sid=AbRjJR; Hm_lvt_0233b908b2bf29bfd788abd7ee3556da=1514949857,1517319361,1517404341,1517531063; Hm_lpvt_0233b908b2bf29bfd788abd7ee3556da=1517531983',
                  'Cookie': '__jsluid=6929a630bc56ed6c957b26af2da5729a; CNZZDATA1261728527=291603669-1495773261-%7C1509435159; tb_history=jPSj5I; 55188_passport=9ONdxrpBaQXdm5bJmldyW5FlxidRvMBqAr4yIAEPqpE2gxZrwiXjZrr2pMwUIZJzKxpiUDVxAArpfhaM0bIVIV0TZmuoICVXTlBCJt8Vwg1t0n%2Fs03UlkW98jxCmFh7rAzHcFxrAgMlYqHym64LCa58VKIo03QxlO9imPGSBiw8%3D; cdb2_auth=23yq1zfEU4FHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Iu%2BD; cdb2_auth=iSj81GKfVYBHLYUBsReMjG%2F%2Fx1MorJ1bXgz31RCEePY3Ry9RF%2BnqADq%2BUOOor6g5Ig; 55188_live_auth=%2Bk62eHaAzpL1S9cCt2328eky56F6xHhgISWBABplU%2Bp5cbfGJnmHjGtFbhjVtcd58vSnUxgfgP%2FWNnMKstiQyNqIuNrjFq%2FYmHxFSMihqfTxgEboKd9p9tA0Mxvidv8dpb%2FWwOUe5w15c3JMsPNAcu9szA3Cr35doDO7FSL9l2E%3D; cdb2_visitedfid=8D102D45; cdb2_fid8=1517788455; cdb2_oldtopics=D7978523D8267455D8103863D8131408D; tmc=3.163970043.43951119.1517791782140.1517791785984.1517791942559; tma=163970043.95102231.1517532552146.1517532552146.1517791782144.2; tmd=13.163970043.95102231.1517532552146.; fingerprint=cffb45388c4fa9828c85417d56c002af; bfd_s=243350108.104448423711421.1517791782148; bfd_g=9ad302420a01281e00002480000219025927b43a; cdb2_sid=20Kv0p; Hm_lvt_0233b908b2bf29bfd788abd7ee3556da=1517319361,1517404341,1517531063,1517791725; Hm_lpvt_0233b908b2bf29bfd788abd7ee3556da=1517792082',
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
    print(links)
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