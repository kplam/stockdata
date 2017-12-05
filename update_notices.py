#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""
from kpfunc.spyder import spyder
from kpfunc.getdata import localconn,serverconn
from time import sleep
from random import random
import datetime
import pandas as pd
import json,re

def notices(conn=localconn(),proxy=0):
    url = "http://data.eastmoney.com/notices/getdata.ashx?FirstNodeType=0&CodeType=1&PageIndex=1&PageSize=4000"
    html =spyder(url,proxy=proxy)
    pass

"""
  // 【返回数据字段：NOTICEDATE, NOTICETITLE, INFOCODE, ANN_RELCOLUMNS.COLUMNNAME, CDSY_SECUCODES.SECURITYCODE, CDSY_SECUCODES.SECURITYSHORTNAME, CDSY_SECUCODES.SECURITYTYPECODE, CDSY_SECUCODES.TRADEMARKETCODE】
                // 【数据字段含义：公告日期,   公告标题,    资讯编码, 公告类型,                  股票代码,                    股票简称,                         股票类型代码,                        交易所代码】

"""