from kpfunc.getdata import *
import pandas as pd
import datetime,time,random
from cal_financial import *
from bs4 import BeautifulSoup as bs


def cal_code(N=0):
    findate = '2017-09-30'
    forecastdate = '2017-12-31'
    tamodel = 'all' #(all,1,2)
    blockdays = 60
    lhbdays = 60
    spodays = 365*3
    modays = 60
    zzddays = 30
    lastdate = datetime.date.today()-datetime.timedelta(days=N)
    basesub = ['fr', 'fmedian', 'forecast', 'spo']
    hotsub = ['mo', 'blocktrade', 'lhb', 'zzd','unusual']
    tradesub = ['useful']
    sub = basesub + tradesub #+ [random.choice(randomsub)]
    # sub = tradesub



    conn = localconn()
    alllist =[]
    result =[]
    if N==0 and int():
        sql_date = "select distinct `date` from `indexdb` ORDER BY `date` DESC limit 1"
        lastdate = pd.read_sql(sql_date,conn)['date'].values[0]
    stocklist = get_df_stocklist()

    ## financial rank
    def fr(findate):
        sql_fr = "select * from `financial_rank` WHERE `总评分`>63 and `报表日期`='%s'" % (findate)
        list_fr = pd.read_sql(sql_fr, conn)['代码'].values
        return list_fr

    ## financial median model
    def fmedian():
        return cal_financial(localconn()).median()

    ## usefuldata
    def useful(tamodel='all'):
        sql_useful = "select * from `usefuldata` WHERE `date`='%s' and `taresult`!='0' and `amorank`<=800 and `araise`<=-120" % (
        lastdate)
        df_useful = pd.read_sql(sql_useful, conn)
        list_useful_model1 = df_useful[(df_useful['taresult'] == '1') | (df_useful['taresult'] == '1,2')]['code'].values
        list_useful_model2 = df_useful[(df_useful['taresult'] == '2') | (df_useful['taresult'] == '1,2')]['code'].values
        list_useful = df_useful['code'].values
        if tamodel == 'all':
            return list_useful
        if tamodel == '1':
            return list_useful_model1
        if tamodel == '2':
            return list_useful_model2

    ## forecast
    def forecast(forecastdate):
        sql_forecast = "select * from `forecast` WHERE `同期净利润`>10000000 and `上限`>30 and `财报日期`='%s'" %(forecastdate)
        list_forecast = pd.read_sql(sql_forecast,conn)['code'].values
        return list_forecast

    def blocktrade(blockdays):
        sql_blocktrade = "select `code` from `blocktrade` where `成交价`>`收盘价` and `交易日期`>='%s' and `交易日期`<='%s' " % (
        lastdate - datetime.timedelta(days=blockdays), lastdate)
        list_blocktrade = pd.read_sql(sql_blocktrade, conn)['code'].values
        return list(set(list_blocktrade))

    def lhb(lhbdays):
        sql_lhbase = "select * from `lhb_base` WHERE `级别`<3"
        xwcode = pd.read_sql(sql_lhbase,conn)['营业部代码'].values
        xw = ','.join(xwcode)+ ',200513872'
        sql_lhb = "select * from `lhb` WHERE `date`>='%s' and  `date`<='%s' and `买卖方向`='1' and `营业部代码` in (%s)  and `买入金额`>1000 ORDER BY `买入金额` DESC "%(lastdate-datetime.timedelta(days=lhbdays),lastdate,xw)
        df_lhb = pd.read_sql(sql_lhb,conn)
        list_lhb = list(set(df_lhb['code'].values))
        return list_lhb

    def spo(spodays):
        sql_spo = "select `code` from `spo_done` WHERE `发行日期`>'%s' and `发行日期`<='%s'" %(lastdate-datetime.timedelta(days=spodays),lastdate)
        list_spo = pd.read_sql(sql_spo,conn)['code'].values
        return list(set(list_spo))

    def mo(modays):
        sql_mo = "select * from `managerial` WHERE `日期`>'%s' and `日期`<='%s'" % (
        lastdate - datetime.timedelta(days=modays), lastdate)
        df_mo = pd.read_sql(sql_mo, conn)
        codes = list(set(df_mo['code'].values))
        list_mo = []
        for code in codes:
            if df_mo[df_mo['code'] == code]['变动股数'].sum() > 0:
                list_mo.append(code)
        return list_mo

    def zzd(zzddays):
        sql = "select * from `news` WHERE `source`='zf826.com' and `datetime`>='%s'" % (lastdate-datetime.timedelta(days=zzddays))
        df = pd.read_sql(sql, localconn())['content']
        s = ''
        for i in range(len(df)):
            s = s + bs(df[i], 'html5lib').text
        zzd_result = []
        for i in range(len(stocklist)):
            code = stocklist['证券代码'][i]
            name = stocklist['证券简称'][i]
            times = s.count(name)
            if times > 1:
                zzd_result.append([code, name, times])
        df_zzd = pd.DataFrame(zzd_result, columns=['code', 'name', 'times'])
        df_zzd = df_zzd.sort_values('times',ascending=False).reset_index(drop=True)
        return df_zzd['code'].values

    def unusual(day=0,ipo=180):
        sql = "select * from `unusual` WHERE `datetime` >='%s' and `goodorbad` = 1" % (
                datetime.date.today() - datetime.timedelta(days=day))
        df = pd.read_sql(sql, localconn())
        df2 = df['code'].value_counts()
        df2 = pd.DataFrame(df2).reset_index().rename(columns={'index': 'code', 'code': 'times'})
        ref = int(df2['times'].median() + df2['times'].std())

        result = []
        for i in range(len(df2)):
            code = df2['code'][i]
            times = df2['times'][i]
            if code[0] in ['6', '0', '3'] and times > ref:
                sqlcheck = "select `证券简称`,`首发日期` from `basedata` WHERE `证券代码`='%s'" % (code)
                df_check = pd.read_sql(sqlcheck, localconn())
                if df_check.empty == False:
                    if df_check['首发日期'][0] < (datetime.date.today() - datetime.timedelta(days=ipo)):
                        result.append([code, df_check['证券简称'][0], times])
                else:
                    print(code)

        df3 = pd.DataFrame(result, columns=['code', 'name', 'times'])
        return df3['code'].values

    if 'fr' in sub:
        alllist.append(fr(findate))

    if 'fmedian' in sub:
        alllist.append(fmedian())

    if 'useful' in sub:
        alllist.append(useful(tamodel))

    if 'forecast' in sub:
        alllist.append(forecast(forecastdate))

    if 'blocktrade' in sub:
        alllist.append(blocktrade(blockdays))

    if 'lhb' in sub:
        alllist.append(lhb(lhbdays))

    if 'spo' in sub:
        alllist.append(spo(spodays))

    if 'mo' in sub:
        alllist.append(mo(modays))

    if 'zzd' in sub:
        alllist.append(zzd(zzddays))

    if 'unusual' in sub:
        alllist.append(unusual())

    ## update_tdxblock
    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\JSC.blk", 'w+') as f:
        list_useful = useful(tamodel='all')
        for code in list_useful:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\LHB.blk", 'w+') as f:
        list_lhb_tdx =lhb(N)
        for code in list_lhb_tdx:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\DZJY.blk", 'w+') as f:
        list_blocktrade_tdx = blocktrade(N)
        for code in list_blocktrade_tdx:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\GPC.blk", 'w+') as f:
        baselist = [fr(findate),fmedian(),forecast(forecastdate=forecastdate),spo(spodays)]
        gpc=[]
        for i, stocks in enumerate(baselist):
            if i == 0:
                gpc = stocks
            else:
                gpc = list(set(gpc).intersection(stocks))
        for code in gpc:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\ZZD.blk", 'w+') as f:
        zzdlist =zzd(0)
        for code in zzdlist:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\GGZC.blk", 'w+') as f:
        mo_list = mo(7)
        for code in mo_list:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\JYYD.blk", 'w+') as f:
        unusual_list = unusual()
        for code in unusual_list:
            if code[0] == '6':
                f.write('1' + code + '\n')
            else:
                f.write('0' + code + '\n')

    for i,stocks in enumerate(alllist):
        if i==0:
            result = stocks
        else:
            result = list(set(result).intersection(stocks))

    print(lastdate)
    if len(result) > 0:
        print("共选出%i只个股" % len(result))
        with open(r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\%s.blk" % (str(lastdate)[8:10]),'w+') as f:
            for code in result:
                name = stocklist[stocklist['证券代码']==code]['证券简称'].values[0]
                print(code,name)
                if code[0] == '6':
                    f.write('1' + code + '\n')
                else:
                    f.write('0' + code + '\n')
    else:
        print("共选出%i只个股" % len(result))

if __name__ == '__main__':
    cal_code(N=0)
