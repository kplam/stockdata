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

def spo(conn=localconn(),proxy=0):
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&p=1&ps=4000"
    html =spyder(url,proxy=proxy)
    pass

"""

"""