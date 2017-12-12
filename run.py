from gevent.pool import Pool
import gevent
import datetime,time
from kpfunc.getdata import localconn
import pandas as pd


while True:

    gpool = Pool(5)
    tasks =[]
    now = int(time.strftime("%H%M%S"))

    status_save_unusual = 0
    status_update_ftsplit = 0
    status_update_dayline = 0
    status_caldatas = 0
    status_update_lhb = 0
    status_update_bloktrade = 0
    status_update_spo = 0
    status_update_stocklist = 0
    status_update_basedata = 0
    status_update_mo = 0

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


    def run_stocklist():
        global status_update_stocklist
        try:
            update_stocklist()
            status_update_stocklist = 1
        except Exception as e:
            print(e)
            status_update_stocklist = 9

    def run_mo():
        global status_update_mo
        pages = range(1, 2)
        try:
            mo(pages)
            status_update_mo = 1
        except Exception as e:
            print(e)
            status_update_mo = 9

    def run_lhb():
        global status_update_lhb
        try:
            lhb()
            status_update_lhb = 1
        except Exception as e:
            print(e)
            status_update_lhb = 9

    def run_blocktrade():
        global status_update_bloktrade
        list_date = [datetime.date.today()]
        try:
            get_blocktrade(list_date)
            status_update_bloktrade = 1
        except Exception as e:
            print(e)
            status_update_bloktrade = 9

    def run_spo():
        global status_update_spo
        try:
            spo()
            status_update_spo = 1
        except Exception as e:
            print(e)
            status_update_spo = 9

    def run_caldatas():
        global status_caldatas
        try:
            calc().amorank()
            status_caldatas = 1
        except Exception as e:
            print(e)
            status_caldatas = 9

    def run_dayline():
        try:
            update_bar().update_stock()
            print("Update stock daybar done!")
            update_bar().update_index()
            print("Update index daybar done!")
            update_bar().update_stock_status()
            print('Update Stock Status Done!')
            status_update_dayline = 1
        except Exception as e:
            print(e)
            #  send email to kplam@qq.com
            status_update_dayline = 9
        return status_update_dayline

    def run_ftsplit():
        global status_update_ftsplit
        try:
            status_update_ftsplit = ftsplit()
            status_update_ftsplit = 1
        except Exception as e:
            print(e)
            status_update_ftsplit = 9

    def run_unusual():
        global status_save_unusual
        try:
            analysis()
            status_save_unusual = 1
        except Exception as e:
            print(e)
            status_save_unusual = 9

    def run_basedata():
        global status_update_basedata
        try:
            sql = "SELECT `证券代码`,`证券简称` FROM `basedata` WHERE `公司名称` IS NULL or `核心题材`='<p>该品种暂无此项记录!</p>'"
            stocklist = pd.read_sql(sql, localconn())
            times_retry = 10
            while len(stocklist) > 0 and times_retry != 0:
                stocklist = update_embasedata(stocklist, "local", 0)
                times_retry -= 1
            status_update_basedata = 1
        except Exception as e:
            print(e)
            status_update_basedata = 9

    def run_notices():
        pages = range(1, 3)[::-1]
        times_retry = 3
        while len(pages) != 0 and times_retry != 0:
            pages = [notices(page) for page in pages]
            pages = list(set(pages))
            pages.remove(None)
            times_retry -= 1

    if now % 100 == 0: # news
        from update_news import stcn_news
        tasks.append(gpool.spawn(stcn_news))
        from update_newscontent import news_content
        tasks.append(gpool.spawn(news_content))

    if now % 10000 == 0: # forecast
        from update_forecast import get_forecast
        tasks.append(gpool.spawn(get_forecast))

    if now % 20000 == 0: # notices
        tasks.append(run_notices)

    if now >= 120000 and status_update_basedata == 0:  # basedata
        tasks.append(gpool.spawn(run_basedata))
    elif now < 90000 and status_save_unusual != 0:
        status_update_basedata = 0

    if datetime.date.today().weekday() < 5:

        if now >= 151500 and status_save_unusual == 0: # unusual
            tasks.append(gpool.spawn(run_unusual))
        elif now < 90000 and status_save_unusual != 0:
            status_save_unusual = 0

        if now >= 153000 and status_update_ftsplit == 0 : # ftsplit
            tasks.append(gpool.spawn(run_ftsplit))
        elif now < 90000 and status_update_ftsplit !=0 :
            status_update_ftsplit = 0

        if now >= 160000 and status_update_dayline == 0: # stock daybar

            tasks.append(gpool.spawn(run_dayline))
        elif now < 90000 and status_update_dayline != 0:
            status_update_dayline = 0

        if now >= 163000 and status_update_dayline == 1 and  status_caldatas == 0: # cal_data
            tasks.append(gpool.spawn(run_caldatas))
        elif now<90000 and status_caldatas != 0:
            status_caldatas = 0

        if  now >= 170000 and status_update_spo == 0 : #spo
            tasks.append(gpool.spawn(run_spo))
        elif now < 90000 and status_update_spo != 0:
            status_update_spo = 0

        if now >= 190000 and status_update_bloktrade == 0 : # blocktrade
            tasks.append(gpool.spawn(run_blocktrade))
        elif now < 90000 and status_update_bloktrade != 0:
            status_update_bloktrade =0

        if now >= 190000 and status_update_lhb == 0: #lhb
            tasks.append(gpool.spawn(run_lhb))
        elif now < 90000 and status_update_lhb != 0:
            status_update_lhb = 0

        if now >= 193000 and status_update_mo == 0: # managerial_ownership
            tasks.append(gpool.spawn(run_mo))
        elif now < 90000 and status_update_mo != 0:
            status_update_mo = 0

    if now >= 200000 and status_update_stocklist == 0 : #stocklist
        tasks.append(gpool.spawn(run_stocklist))
    elif now < 90000 and status_update_stocklist != 0:
        status_update_stocklist = 0

    if now >= 220000:
        if status_save_unusual == 9 :
            tasks.append(gpool.spawn(run_unusual))
        if status_update_ftsplit == 9 :
            tasks.append(gpool.spawn(run_ftsplit))
        if status_update_dayline == 9 :
            tasks.append(gpool.spawn(run_dayline))
        if status_caldatas == 9 :
            tasks.append(gpool.spawn(run_caldatas))
        if status_update_lhb == 9 :
            tasks.append(gpool.spawn(run_lhb))
        if status_update_bloktrade == 9 :
            tasks.append(gpool.spawn(run_blocktrade))
        if status_update_spo == 9 :
            tasks.append(gpool.spawn(run_spo))
        if status_update_stocklist == 9 :
            tasks.append(gpool.spawn(run_stocklist))
        if status_update_basedata == 9 :
            tasks.append(gpool.spawn(run_basedata))
        if status_update_mo == 9 :
            tasks.append(gpool.spawn(run_mo))

    gevent.joinall(tasks)