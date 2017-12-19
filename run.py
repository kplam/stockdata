#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-10

@author: kplam
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import datetime,time,warnings,gc,os
from kpfunc.getdata import localconn
import pandas as pd
from update_news import stcn_news
from update_newscontent import news_content
from update_notices import notices
from update_basedata import update_embasedata
from save_unusual import analysis
from update_ftsplit import ftsplit
from update_dayline import update_bar
from cal_datas import calc
from update_spo import spo
from update_blocktrade import get_blocktrade
from update_lhb import lhb
from update_managerial_ownership import mo
from update_stocklist import update_stocklist
from update_forecast import get_forecast
from update_tickdata import update_tick



BS = BlockingScheduler()

@BS.scheduled_job('interval', max_instances=10, minutes=1, id='run_news')
def run_news():
    stcn_news()
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, minutes=2, id='run_newscontent')
def run_newscontent():
    news_content()
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, hours=2, id='run_forecast')
def run_forecast():
    print("Forecast...")
    get_forecast()
    gc.collect()


@BS.scheduled_job('interval', max_instances=10, hours=2,id='run_notices')
def run_notices():
    try:
        notices(1,localconn(),0)
    except Exception as e:
        print(e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, hours=4,id='run_basedata')
def run_basedata():
    try:
        sql = "SELECT `证券代码`,`证券简称` FROM `basedata` WHERE `公司名称` IS NULL or `核心题材`='<p>该品种暂无此项记录!</p>'"
        stocklist = pd.read_sql(sql, localconn())
        times_retry = 10
        while len(stocklist) > 0 and times_retry != 0:
            stocklist = update_embasedata(stocklist, "local", 0)
            times_retry -= 1
    except Exception as e:
        print("Basedata:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, hour=20,id='run_stocklist')
def run_stocklist():
    try:
        update_stocklist()
    except Exception as e:
        print("Stocklist:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, hour=20,id='run_mo')
def run_mo():
    pages = range(1, 2)
    try:
        mo(pages)
    except Exception as e:
        print("MO:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=18,minute=30,id='run_lhb')
def run_lhb():
    try:
        lhb()
    except Exception as e:
        print("LHB:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=19,minute=00,id='run_blocktrade')
def run_blocktrade():
    list_date = [datetime.date.today()]
    try:
        get_blocktrade(list_date)
    except Exception as e:
        print("blocktrade:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=18,minute=00,id='run_spo')
def run_spo():
    try:
        spo()
    except Exception as e:
        print("spo:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=15,minute=15,id='run_tick')
def run_tick():
    try:
        update_tick(500)
    except Exception as e:
        print("Tick:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=16,minute=30,id='run_caldatas')
def run_caldatas():
    try:
        calc().amorank()
    except Exception as e:
        print("caldatas:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=16,minute=00,id='run_dayline')
def run_dayline():
    try:
        update_bar().update_stock()
        print("Update stock daybar done!")
        update_bar().update_index()
        print("Update index daybar done!")
        update_bar().update_stock_status()
        print('Update Stock Status Done!')
    except Exception as e:
        print("Dayline:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=15,minute=30,id='run_ftsplit')
def run_ftsplit():
    try:
        ftsplit()
    except Exception as e:
        print("ftsplit:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour='9,10,11,13,14,15',minute='*/2',id='run_unusual')
def run_unusual():
    try:
        analysis()
    except Exception as e:
        print("unusual:",e)
    gc.collect()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    BS.start()
