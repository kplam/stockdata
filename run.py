#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-10

@author: kplam
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import datetime,time,warnings
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

# status_save_unusual = 1
# status_update_ftsplit = 1
# status_update_dayline = 0
# status_caldatas = 0
# status_update_lhb = 0
# status_update_bloktrade = 0
# status_update_spo = 0
# status_update_stocklist = 0
# status_update_basedata = 1
# status_update_mo = 0

@BS.scheduled_job('interval',minutes=1,id='run_news')
def run_news():
    stcn_news()

@BS.scheduled_job('interval',minutes=1,id='run_newscontent')
def run_newscontent():
    news_content()

@BS.scheduled_job('interval',hours=1,id='run_forecast')
def run_forecast():
    print("Forecast...")
    get_forecast()

@BS.scheduled_job('interval',hours=2,id='run_notices')
def run_notices():
    pages = range(1, 3)[::-1]
    times_retry = 3
    while len(pages) != 0 and times_retry != 0:
        pages = [notices(page) for page in pages]
        pages = list(set(pages))
        pages.remove(None)
        times_retry -= 1

@BS.scheduled_job('interval',hours=8,id='run_notices')
def run_basedata():
    # global status_update_basedata
    try:
        sql = "SELECT `证券代码`,`证券简称` FROM `basedata` WHERE `公司名称` IS NULL or `核心题材`='<p>该品种暂无此项记录!</p>'"
        stocklist = pd.read_sql(sql, localconn())
        times_retry = 10
        while len(stocklist) > 0 and times_retry != 0:
            stocklist = update_embasedata(stocklist, "local", 0)
            times_retry -= 1
        # status_update_basedata = 1
    except Exception as e:
        print("Basedata:",e)
        # status_update_basedata = 9

@BS.scheduled_job('cron',hour=20,id='run_stocklist')
def run_stocklist():
    # global status_update_stocklist
    try:
        update_stocklist()
        # status_update_stocklist = 1
    except Exception as e:
        print("Stocklist:",e)
        # status_update_stocklist = 9

@BS.scheduled_job('cron',hour=20,id='run_mo')
def run_mo():
    # global status_update_mo
    pages = range(1, 2)
    try:
        mo(pages)
        # status_update_mo = 1
    except Exception as e:
        print("MO:",e)
        # status_update_mo = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=18,minute=30,id='run_lhb')
def run_lhb():
    # global status_update_lhb
    try:
        lhb()
        # status_update_lhb = 1
    except Exception as e:
        print("LHB:",e)
        # status_update_lhb = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=19,minute=00,id='run_blocktrade')
def run_blocktrade():
    # global status_update_bloktrade
    list_date = [datetime.date.today()]
    try:
        get_blocktrade(list_date)
        # status_update_bloktrade = 1
    except Exception as e:
        print("blocktrade:",e)
        # status_update_bloktrade = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=18,minute=00,id='run_spo')
def run_spo():
    # global status_update_spo
    try:
        spo()
        # status_update_spo = 1
    except Exception as e:
        print("spo:",e)
        # status_update_spo = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=15,minute=15,id='run_tick')
def run_tick():
    try:
        update_tick(500)
    except Exception as e:
        print("Tick:",e)

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=16,minute=30,id='run_caldatas')
def run_caldatas():
    # global status_caldatas
    try:
        calc().amorank()
        # status_caldatas = 1
    except Exception as e:
        print("caldatas:",e)
        # status_caldatas = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=16,minute=00,id='run_dayline')
def run_dayline():
    # global status_update_dayline
    try:
        update_bar().update_stock()
        print("Update stock daybar done!")
        update_bar().update_index()
        print("Update index daybar done!")
        update_bar().update_stock_status()
        print('Update Stock Status Done!')
        # status_update_dayline = 1
    except Exception as e:
        print("Dayline:",e)
        #  send email to kplam@qq.com
        # status_update_dayline = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=15,minute=30,id='run_ftsplit')
def run_ftsplit():
    # global status_update_ftsplit
    try:
        ftsplit()
        # status_update_ftsplit = 1
    except Exception as e:
        print("ftsplit:",e)
        # status_update_ftsplit = 9

@BS.scheduled_job('cron',day_of_week='mon-fri',hour=15,minute=15,id='run_unusual')
def run_unusual():
    # global status_save_unusual
    try:
        analysis()
        # status_save_unusual = 1
    except Exception as e:
        print("unusual:",e)
        # status_save_unusual = 9


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    BS.start()

# if now % 20000 == 0: # forecast
#     tasks.append(gpool.spawn(get_forecast))
#     print("Forecast is running!")

# if now % 20000 == 0: # notices
#     tasks.append(gpool.spawn(run_notices))
#     print("Notices is running!")

# if now >= 120000 and status_update_basedata == 0:  # basedata
#     tasks.append(gpool.spawn(run_basedata))
#     print("Basedata is running!")
# elif now < 90000 and status_update_basedata != 0:
#     status_update_basedata = 0
#
# if datetime.date.today().weekday() < 5:
#
#     if now >= 151500 and status_save_unusual == 0: # unusual
#         tasks.append(gpool.spawn(run_unusual))
#         print("Unusual is running!")
#     elif now < 90000 and status_save_unusual != 0:
#         status_save_unusual = 0
#
#     if now >= 153000 and status_update_ftsplit == 0 : # ftsplit
#         tasks.append(gpool.spawn(run_ftsplit))
#         print("Ftsplit is running!")
#     elif now < 90000 and status_update_ftsplit !=0 :
#         status_update_ftsplit = 0
#
#     if now >= 160000 and status_update_dayline == 0: # stock daybar
#         tasks.append(gpool.spawn(run_dayline))
#         print("Dayline is running!")
#     elif now < 90000 and status_update_dayline != 0:
#         status_update_dayline = 0
#
#     if now >= 163000 and status_update_dayline == 1 and  status_caldatas == 0: # cal_data
#         tasks.append(gpool.spawn(run_caldatas))
#         print("Caldatas is running!")
#     elif now<90000 and status_caldatas != 0:
#         status_caldatas = 0
#
#     if  now >= 170000 and status_update_spo == 0 : #spo
#         tasks.append(gpool.spawn(run_spo))
#         print("Spo is running!")
#     elif now < 90000 and status_update_spo != 0:
#         status_update_spo = 0
#
#     if now >= 190000 and status_update_bloktrade == 0 : # blocktrade
#         tasks.append(gpool.spawn(run_blocktrade))
#         print("Blocktrade is running!")
#     elif now < 90000 and status_update_bloktrade != 0:
#         status_update_bloktrade =0
#
#     if now >= 190000 and status_update_lhb == 0: #lhb
#         tasks.append(gpool.spawn(run_lhb))
#         print("Lhb is running!")
#     elif now < 90000 and status_update_lhb != 0:
#         status_update_lhb = 0
#
#     if now >= 193000 and status_update_mo == 0: # managerial_ownership
#         tasks.append(gpool.spawn(run_mo))
#         print("Mo is running!")
#     elif now < 90000 and status_update_mo != 0:
#         status_update_mo = 0
#
# if now >= 200000 and status_update_stocklist == 0 : #stocklist
#     tasks.append(gpool.spawn(run_stocklist))
#     print("Stocklist is running!")
# elif now < 90000 and status_update_stocklist != 0:
#     status_update_stocklist = 0

# if now >= 220000:
#     print("Error checking!")
#     if status_save_unusual == 9 :
#         tasks.append(gpool.spawn(run_unusual))
#     if status_update_ftsplit == 9 :
#         tasks.append(gpool.spawn(run_ftsplit))
#     if status_update_dayline == 9 :
#         tasks.append(gpool.spawn(run_dayline))
#     if status_caldatas == 9 :
#         tasks.append(gpool.spawn(run_caldatas))
#     if status_update_lhb == 9 :
#         tasks.append(gpool.spawn(run_lhb))
#     if status_update_bloktrade == 9 :
#         tasks.append(gpool.spawn(run_blocktrade))
#     if status_update_spo == 9 :
#         tasks.append(gpool.spawn(run_spo))
#     if status_update_stocklist == 9 :
#         tasks.append(gpool.spawn(run_stocklist))
#     if status_update_basedata == 9 :
#         tasks.append(gpool.spawn(run_basedata))
#     if status_update_mo == 9 :
#         tasks.append(gpool.spawn(run_mo))


