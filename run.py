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
from update_zzd import get_zzd,get_urllist_one
from update_managerial_ownership import mo
from update_stocklist import update_stocklist
from update_forecast import get_forecast
from update_tickdata import update_tick,zipfiles
from statistics import cal_statistics
from email_warning import sendmail
from update_focus import update_focussql
from update_mainbusiness import mainbusiness
from update_shareholder import get_shareholder_data
from update_is import get_all_is_date, errorretry, cal_datelist

BS = BlockingScheduler()

@BS.scheduled_job('cron', max_instances=20, hour='8-23', minute='*/1', id='run_news')
def run_news():
    try:
        stcn_news()
    except Exception as e:
        print("news:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, hour='8-23', minute='*/2', id='run_newscontent')
def run_newscontent():
    try:
        news_content()
    except Exception as e:
        print("newscontent:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=20, hours=2, id='run_forecast')
def run_forecast():
    try:
        get_forecast(proxy=0,lastday=0,update=1)
    except Exception as e:
        print("forecast:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=20, hours=2,id='run_notices')
def run_notices():
    try:
        notices(1,proxy=0)
    except Exception as e:
        print("notice:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri', hour=6,id='run_basedata')
def run_basedata():
    try:
        sql = "SELECT `证券代码`,`证券简称` FROM `basedata` WHERE `公司名称` IS NULL or `核心题材`='<p>该品种暂无此项记录!</p>'"
        stocklist = pd.read_sql(sql, conn())
        times_retry = 10
        while len(stocklist) > 0 and times_retry != 0:
            stocklist = update_embasedata(stocklist, ser='local', proxy=0)
            times_retry -= 1
    except Exception as e:
        print("Basedata:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, hour='8,12,20',id='run_stocklist')
def run_stocklist():
    try:
        update_stocklist(proxy=0)
    except Exception as e:
        print("Stocklist:",e)
    gc.collect()

@BS.scheduled_job('interval', max_instances=20, hours=3,id='run_mo')
def run_mo():
    try:
        mo([1], proxy=0)
    except Exception as e:
        print("MO:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=18,minute=30,id='run_lhb')
def run_lhb():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        sqlcheck = "select `date` from `lhb` WHERE `date`='%s' LIMIT 1"%(datetime.date.today())
        # scheck = pd.read_sql(sqlcheck,serverconn())
        lcheck = pd.read_sql(sqlcheck,conn())
        times_retry = 5
        while lcheck.empty == True and times_retry != 0:
        # while (scheck.empty == True or lcheck.empty == True) and times_retry != 0:
            try:
                # if scheck.empty == True and lcheck.empty == True:
                #     lhb(ser='both')
                # elif scheck.empty == True and lcheck.empty == False:
                #     lhb(ser='server')
                # elif scheck.empty == False and lcheck.empty == True:
                lhb()
            except Exception as e:
                if times_retry == 1:
                    sendmail("LHB Update Failed", str(datetime.date.today())+str(e))
                print("LHB:", e)
            finally:
                # scheck = pd.read_sql(sqlcheck, serverconn())
                lcheck = pd.read_sql(sqlcheck, conn())
                times_retry -= 1
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=19,minute=00,id='run_blocktrade')
def run_blocktrade():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        list_date = [datetime.date.today()]
        sqlcheck = "select `交易日期` from `blocktrade` WHERE `交易日期`='%s' LIMIT 1"%(str(list_date[0]))
        # scheck = pd.read_sql(sqlcheck,serverconn())
        lcheck = pd.read_sql(sqlcheck,conn())
        times_retry = 5
        # while (scheck.empty == True or lcheck.empty == True) and times_retry != 0:
        while lcheck.empty == True and times_retry != 0:
            try:
                # if scheck.empty == True and lcheck.empty == True:
                #     get_blocktrade(list_date,ser='both',proxy=0)
                # elif scheck.empty ==True and lcheck.empty == False:
                #     get_blocktrade(list_date,ser='server',proxy=0)
                # elif scheck.empty ==False and lcheck.empty == True:
                get_blocktrade(list_date,ser='local',proxy=0)
            except Exception as e:
                if times_retry == 1:
                    sendmail("Blocktrade Update Failed",str(datetime.date.today())+str(e))
                print("blocktrade:",e)
            finally:
                # scheck = pd.read_sql(sqlcheck, serverconn())
                lcheck = pd.read_sql(sqlcheck, conn())
                times_retry -= 1
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour='18,20,22',minute=10,id='run_spo')
def run_spo():
    try:
        spo(proxy=0)
    except Exception as e:
        sendmail('spo', str(e))
        print("spo:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=16,minute=15,id='run_zdt')
def run_zdt():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        from update_ztdt import updatesql_all
        try:
            updatesql_all()
        except Exception as e:
            sendmail('ztdt',str(e))
            print("ZTDT:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=15,minute=15,id='run_tick')
def run_tick():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        try:
            update_tick(500)
            zipfiles()
        except Exception as e:
            print("Tick:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=16,minute=45,id='run_statistics')
def get_statistics():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        sqlcheck = "select * from `statistics` WHERE `date` = '%s'"%(str(datetime.date.today()))
        # sdfcheck = pd.read_sql(sqlcheck,serverconn())
        ldfcheck = pd.read_sql(sqlcheck,conn())
        times_retry = 5
        # while (sdfcheck.empty == True or ldfcheck.empty == True) and times_retry !=0:
        while ldfcheck.empty == True and times_retry != 0:
            try:
                # if sdfcheck.empty == True and ldfcheck.empty == True:
                #     cal_statistics(ser='both')
                # elif sdfcheck.empty == True and ldfcheck.empty == False:
                #     cal_statistics(ser='server')
                # elif sdfcheck.empty == False and ldfcheck.empty == True:
                cal_statistics()
            except Exception as e:
                if times_retry == 1:
                    sendmail("Statistics Update Error!",str(datetime.date.today())+str(e))
                print("statistics:",e)
            finally:
                # sdfcheck = pd.read_sql(sqlcheck, serverconn())
                ldfcheck = pd.read_sql(sqlcheck, conn())
                times_retry -= 1
        # if sdfcheck['ontrade'][0] <3000 or ldfcheck['ontrade'][0]<3000 or sdfcheck['ontrade'][0] != ldfcheck['ontrade'][0]:
        if ldfcheck['ontrade'][0] < 3000 :

            subject = '【注意】Statistics Error'
            content = '统计出错，请马上检查数据！'
            # if sdfcheck['ontrade'][0] <3000:
            #     subject = subject + ' Server'
            if ldfcheck['ontrade'][0]<3000:
                subject = subject + ' local'
            # if sdfcheck['ontrade'][0] != ldfcheck['ontrade'][0]:
            #     content = content + ' 两地数据不一致!'
            sendmail(subject,str(datetime.date.today())+content)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=16,minute=30,id='run_caldatas')
def run_caldatas():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        sql = "select distinct `date` from `usefuldata` where `date` ='%s'" % (str(datetime.date.today()))
        dfcheckl = pd.read_sql(sql, conn())
        # dfchecks = pd.read_sql(sql, serverconn())

        times_retry= 10
        # while (dfcheckl.empty == True or dfchecks.empty == True) and times_retry != 0:
        while dfcheckl.empty == True and times_retry != 0:

            try:
                # if dfcheckl.empty == True and dfchecks.empty == True:
                #     calc(ser='both').amorank()
                # elif dfcheckl.empty == True and dfchecks.empty == False:
                calc().amorank()
                # elif dfcheckl.empty == False and dfchecks.empty == True:
                #     calc(ser='server').amorank()
            except Exception as e:
                if times_retry == 1:
                    sendmail("Cal_datas Failed",str(datetime.date.today())+str(e))
                    print("caldatas:", e)
                else:
                    pass
            finally:
                dfcheckl = pd.read_sql(sql, conn())
                # dfchecks = pd.read_sql(sql, serverconn())
                times_retry -= 1
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=16,minute=00,id='run_dayline')
def run_dayline():
    holiday =['2017-12-30','2017-12-31','2018-01-01','2018-02-15','2018-02-16','2018-02-17','2018-02-18','2018-02-19',
              '2018-02-20','2018-02-21','2018-04-05','2018-04-06','2018-04-07','2018-04-29','2018-04-30','2018-05-01',
              '2018-06-16','2018-06-17','2018-06-18','2018-09-22','2018-09-23','2018-09-24','2018-10-01','2018-10-02',
              '2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07']
    if str(datetime.date.today()) not in holiday:
        local = conn()
        # server = serverconn()
        sql="select distinct `date` from `dayline` where `date` ='%s'"%(str(datetime.date.today()))
        dfchecklocal =pd.read_sql(sql,local)
        times_retry_local =10
        while dfchecklocal.empty==True and times_retry_local != 0:
            try:
                print("Updating Local Daybar...")
                daybarlocal = update_bar(conn=local)
                daybarlocal.update_stock()
                daybarlocal.update_index()
                daybarlocal.update_stock_status()
            except Exception as e:
                if times_retry_local == 1:
                    sendmail("Local Dayline Update Failed",str(datetime.date.today())+str(e))
                    print("Dayline:", e)
                else:
                    pass
            finally:
                dfchecklocal = pd.read_sql(sql, conn())
                times_retry_local -= 1

        # dfcheckserver =pd.read_sql(sql,serverconn())
        # times_retry_server = 10
        # while dfcheckserver.empty == True and times_retry_server != 0:
        #     try:
        #         print("Updating Server Daybar...")
        #         daybarserver = update_bar(conn=server)
        #         daybarserver.update_stock()
        #         daybarserver.update_index()
        #         daybarserver.update_stock_status()
        #     except Exception as e:
        #         if times_retry_local == 1:
        #             sendmail("Server Dayline Update Failed", str(datetime.date.today())+str(e))
        #             print("Dayline:", e)
        #         else:
        #             pass
        #     finally:
        #         dfcheckserver = pd.read_sql(sql, serverconn())
        #         times_retry_server -= 1
        print("Update Daybar Done!")
    gc.collect()

"""
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
"""

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour=15,minute=30,id='run_ftsplit')
def run_ftsplit():
    try:
        ftsplit()
    except Exception as e:
        print("ftsplit:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-sun',hour='21,22,23',minute='*/15',id='run_focus')
def run_focus():
    try:
        update_focussql()
        print("Focus:%s" % (datetime.datetime.today()))
    except Exception as e:
        print("Focus:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour='20,21,22,23',minute='*/5',id='run_zzd')
def run_zzd():
    try:
        get_zzd(links=get_urllist_one(), check=1, ser='local')
        print("ZZD:%s"%(datetime.datetime.today()))
    except Exception as e:
        print("ZZD:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='mon-fri',hour='9,10,11,13,14,15',minute='*/2',id='run_unusual')
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

@BS.scheduled_job('cron', max_instances=20, day_of_week='sat', hour = '6', id='run_shareholder')
def run_shareholder():
    try:
        stocklist = get_shareholder_data(stocklist=get_stocklist_prefix('sh', 'sz', pre=1))
        times_retry = 10
        while len(stocklist) != 0 and times_retry != 0:
            stocklist = get_shareholder_data(stocklist=stocklist)
            times_retry -= 1
    except Exception as e:
        print("shareholder:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='sat',hour='16',id='run_mainbusiness')
def run_mainbusiness():

    try:
        stocklist = get_stocklist_prefix('sh', 'sz', 1)
        mainbusiness(stocklist=stocklist)#,ser='both',proxy= 0)
    except Exception as e:
        print("MAINBUSINESS:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='sun',hour='6',id='run_basedata_all')
def run_basedata_all():
    try:
        stocklist = get_df_stocklist()
        times_retry = 10
        while len(stocklist) > 0 and times_retry != 0:
            stocklist = update_embasedata(stocklist, ser='local', proxy=0)
            times_retry -= 1
    except Exception as e:
        print("Basedata:",e)
    gc.collect()

@BS.scheduled_job('cron', max_instances=20, day_of_week='sun',hour='16',id='run_is')
def run_is():
    try:
        errorlist=get_all_is_date(datelist=cal_datelist(type='single'))
        times_retry=3
        while len(errorlist)>0 and times_retry !=0:
            errorlist=errorretry(errorlist)
            times_retry -=1
    except Exception as e:
        print("IS:%s"%(e))
    gc.collect()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    print("Start!")
    BS.start()
