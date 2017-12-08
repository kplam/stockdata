#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22

@author: kplam
"""
import requests as rqs
from requests.adapters import HTTPAdapter
import pandas as pd
from bs4 import BeautifulSoup as bs
import random
import socket, urllib
import multiprocessing

def get_ip_list_online():
    ip_list = []
    for i in range(1,20):
        url = 'http://www.xicidaili.com/wt/%s'%(i)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        web_data = rqs.get(url, headers=headers)
        soup = bs(web_data.text, 'lxml')
        ips = soup.find_all('tr')

        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[5].text+'://'+tds[1].text + ':' + tds[2].text)
    return ip_list

def ip_check(*path):
    # url_list = ['http://www.baidu.com','http://www.sina.com','http://www.qq.com','http://www.163.com','http://www.cntv.cn','http://www.sohu.com','http://www.youku.com']#打算抓取内容的网页
    # url_list =['http://kuaixun.stcn.com/index.shtml','http://www.eastmoney.com/','http://www.sina.com']
    url_list=['http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&id=0000012&page=1&rows=10000&gtvolume=&sort=asc']
    ip_list = get_ip_list_online()
    print(ip_list)
    if len(path)!=0:
        file=path[0]
        iplist2=pd.read_csv(file,names=['ip'])['ip'].values
        for ip in iplist2:
            ip_list.append("http://"+ip)
    iplist_output=[]
    socket.setdefaulttimeout(1)
    for ip in ip_list:
        proxy_ip ={'http':ip}#想验证的代理IP
        try:
            proxy_support = urllib.request.ProxyHandler(proxy_ip)
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64)")]
            urllib.request.install_opener(opener)
            if urllib.request.urlopen(random.choice(url_list)).code==200:
                iplist_output.append(ip)
                print(ip,200)
        except Exception as e:
            print(e)
    return iplist_output

def get_proxy():
    iplist=pd.read_csv('ip.csv')['ip'].values
    return iplist

def spyder(url,proxy):
    """
    :param url: url
    :param proxy: 0 or 1
    :return: html
    """
    ip_proxy = get_proxy()
    ip = random.choice(ip_proxy)
    proxies = {} if proxy == 0 else {'http':ip}

    # ============ requests setting ============= #
    s = rqs.session()
    s.mount('http://', HTTPAdapter(pool_connections=3, pool_maxsize=3, max_retries=10, pool_block=False))
    s.mount('https://', HTTPAdapter(pool_connections=3, pool_maxsize=3, max_retries=10, pool_block=False))
    rqs_header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, compress',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                                '/53.0.2785.104 Safari/537.36 Core/1.53.4033.400 QQBrowser/9.6.12624.400'}
    try:
        if len(proxies) != 0 :
            rqs_url = s.get(url, headers=rqs_header, timeout=10, proxies=proxies)
        else:
            rqs_url = s.get(url, headers=rqs_header, timeout=10)
        rqs_url.raise_for_status()
    except rqs.RequestException as e:
        rqs_url = "error!"
    s.close()
    return rqs_url

if __name__ == '__main__':
    ip_list=ip_check()
    ip_list=pd.DataFrame(ip_list,columns=['ip'])
    ip_list.to_csv('ip.csv')