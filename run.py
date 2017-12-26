#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-10

@author: kplam
"""

import datetime,warnings,gc

from apscheduler.schedulers.blocking import BlockingScheduler

from kpfunc.getdata import *
from kpfunc.function import *

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
from statistics import cal_statistics


BS = BlockingScheduler()

@BS.scheduled_job('interval', max_instances=10, minutes=1, id='run_news')
def run_news():
    try:
        stcn_news()
    except Exception as e:
        print("news:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, minutes=2, id='run_newscontent')
def run_newscontent():
    try:
        news_content()
    except Exception as e:
        print("newscontent:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, hours=2, id='run_forecast')
def run_forecast():
    try:
        get_forecast()
    except Exception as e:
        print("forecast:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=10, hours=2,id='run_notices')
def run_notices():
    try:
        notices(1,localconn(),0)
    except Exception as e:
        print("notice:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri', hour=6,id='run_basedata')
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

@BS.scheduled_job('interval', max_instances=10, hours=8,id='run_mo')
def run_mo():
    try:
        mo([1])
    except Exception as e:
        print("MO:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=18,minute=30,id='run_lhb')
def run_lhb():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        try:
            lhb()
        except Exception as e:
            print("LHB:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=19,minute=00,id='run_blocktrade')
def run_blocktrade():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        list_date = [datetime.date.today()]
        try:
            get_blocktrade(list_date)
        except Exception as e:
            print("blocktrade:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=18,minute=10,id='run_spo')
def run_spo():
    try:
        spo(con=localconn(),proxy=0)
    except Exception as e:
        print("spo:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=15,minute=15,id='run_tick')
def run_tick():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        try:
            update_tick(500)
        except Exception as e:
            print("Tick:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=16,minute=45,id='run_statistics')
def get_statistics():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        try:
            cal_statistics()
        except Exception as e:
            print("statistics:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=16,minute=30,id='run_caldatas')
def run_caldatas():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        try:
            calc().amorank()
        except Exception as e:
            print("caldatas:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=16,minute=00,id='run_dayline')
def run_dayline():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
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

@BS.scheduled_job('cron', max_instances=10, day_of_week='mon-fri',hour=17,minute=45,id='run_tdx')
def run_tdx():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        from update_tdxblock import tdxblock
        try:
            tdxblock(1)
        except Exception as e:
            print("tdx:",e)
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
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        if 92400 <= int(time.strftime("%H%M%S")) <= 151000:
            try:
                analysis()
            except Exception as e:
                print("unusual:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='sat',hour='9',id='run_shareholder')
def run_shareholder():
    from update_shareholder import get_shareholder_data
    try:
        stocklist = get_shareholder_data()
        times_retry = 3
        while len(stocklist) != 0 and times_retry != 0:
            stocklist = get_shareholder_data()
            times_retry -= 1
    except Exception as e:
        print("shareholder:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='sun',hour='12',id='run_mainbusiness')
def run_mainbusiness():
    from update_mainbusiness import mainbusiness
    from kpfunc.getdata import get_stocklist_prefix
    try:
        stocklist = get_stocklist_prefix('sh', 'sz', 1)
        times_retry = 3
        while len(stocklist) != 0 and times_retry != 0:
            stocklist = mainbusiness(stocklist, localconn(), 0)
            times_retry -= 1
        error = pd.DataFrame(stocklist)
        error.to_csv(path() + '/error/update_mainbusiness.csv')
    except Exception as e:
        print("MAINBUSINESS:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=10, day_of_week='sun',hour='9',id='run_basedata_all')
def run_basedata_all():
    try:
        stocklist = get_df_stocklist()
        times_retry = 10
        while len(stocklist) > 0 and times_retry != 0:
            stocklist = update_embasedata(stocklist, "local", 0)
            times_retry -= 1
    except Exception as e:
        print("Basedata:",e)
    gc.collect()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    BS.start()
