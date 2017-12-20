#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
"""
http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=DCSOBS&token=70f12f2f4f091e459a279469fe49eca5&p=1&ps=5000&sr=-1&st=SZZBL&filter=(ReportingPeriod=^2017-06-30^)&cmd=
"""
import datetime
from kpfunc.getdata import *
from kpfunc.spyder import myspyder

def split_szfh(iLong,Quarter,proxy=0):
    today = datetime.date.today()
    try:
        url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=DCSOBS&token=70f12f2f4f091e459a279469fe49eca5&p=1&ps=%s&sr=-1&st=SZZBL&filter=(ReportingPeriod=^%s^)" % (
        iLong, Quarter)
        html = myspyder(url, proxy=0).content.decode('utf-8')
        if html != "[]":
            table = pd.read_json(html, dtype='object')
            table = pd.DataFrame(np.array(table),
                                 columns=['分红计划', 'date', '除权除息日后30日涨幅', 'code', '每股收益', '股权登记日', '股权登记日前10日涨幅', '股息率',
                                          '净利润同比增长', '每股公积金', '每股未分配利润', '市场', '证券名称', '每股净资产', '方案进度', '报表日期',
                                          '业绩被披露日期', '送股比例', '红股', '总股本', '红利', '预案公告日', '预案公告日后10日涨幅', '已除权天数',
                                          '转股比例'])
            table = table[['date', 'code', '红股', '红利']]
            table = table[table['date'] != '-']
            table['date'] = table['date'].astype('datetime64[ns]')
            table = table[table['date'] == today]
            return table
        else:
            return pd.DataFrame()
    except Exception as e:
        print(e)
        return pd.DataFrame()


def split_pg(proxy):  # 配股
    pg_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSA&st=6&sr=true&p=1&ps=5000'
    get_url = "error!"
    times_retry = 10
    pgtable = []
    List_Fin_pg =pd.DataFrame()
    while get_url == "error!" and times_retry != 0:
        get_url = myspyder(pg_url, proxy)
        times_retry = times_retry - 1
    if get_url !="error!":
        try:
            return_list = re.findall("\"(.*?)\"", get_url.text)

            print("FTSPLIT:配股信息查找完毕，正在写入数据库！")
            for i in range(len(return_list)):
                appd = re.split(",", return_list[i])
                pgtable.append(appd)

            pglist = pd.DataFrame(pgtable, columns=['A', 'B', '股票代码', '股票简称', '配售代码', '配售名称', '配股比例（10配）',
                                                    '配股价', '配股前总股本(万股)', '配股总数', '配股后总股本(万股)', '股权登记日',
                                                    '缴款起始日期', '缴款截止日期', '配股上市日', '除权日', '募资总额', '募资净额',
                                                    '承销方式', '公告日', '最新价', 'C'])
            List_Fin_pg = pglist[['股票代码', '配股比例（10配）', '配股价', '除权日']]
        except:
            pass
    return List_Fin_pg

def ftsplit():
    # ============ global define ============== #
    conn = localconn()
    List_stock = get_stocklist()
    iLong = int((round(len(List_stock)/1000,0)+1)*1000)

    # ============== set Quarter================ #
    today = datetime.date.today()
    print("FTSPLIT:今天是",today,".")
    iyear = int(str(today)[0:4])
    imonth = int(str(today)[5:7])
    Q4 = datetime.datetime(iyear-1,12,31).strftime('%Y-%m-%d')
    Q3 = datetime.datetime(iyear-1,9,30).strftime('%Y-%m-%d') if imonth <= 9 else datetime.datetime(iyear,9,30).strftime('%Y-%m-%d')
    Q2 = datetime.datetime(iyear-1,6,30).strftime('%Y-%m-%d') if imonth <= 6 else datetime.datetime(iyear, 6, 30).strftime('%Y-%m-%d')
    Q1 = datetime.datetime(iyear-1,3,31).strftime('%Y-%m-%d') if imonth <= 3 else datetime.datetime(iyear, 3, 31).strftime('%Y-%m-%d')
    List_Quarter =[Q1,Q2,Q3,Q4]
    # ========== 送转分红 ============ #
    df_ftsplit = pd.DataFrame()
    times_retry = 3
    while df_ftsplit.empty == True and times_retry!=0:
        print("FTSPLIT:正在获取分红数据...")
        for Quarter in List_Quarter:
            df_Fin = split_szfh(Quarter=Quarter,iLong=iLong,proxy=0)
            df_ftsplit = pd.concat((df_ftsplit,df_Fin))
        df_ftsplit = pd.DataFrame(np.array(df_ftsplit),columns=['code','红股','红利','date'])
        times_retry = times_retry-1
    print(df_ftsplit)
    if df_ftsplit.empty != True:
        df_ftsplit = df_ftsplit.reset_index(range(len(df_ftsplit)), drop=True)
        for i in range(len(df_ftsplit)):
            code = str(df_ftsplit.get_value(i,'code'))
            sz = float(df_ftsplit.get_value(i,'红股'))
            xj = float(df_ftsplit.get_value(i,'红利'))
            sdate = str(df_ftsplit.get_value(i,'date'))
            sql_param=(code,sz,xj,sdate)
            sql_update = "INSERT IGNORE INTO `ftsplit`(`code`, `红股`, `红利`,`date`) VALUES (%s,%s,%s,%s)"
            cur = conn.cursor()
            cur.execute(sql_update,sql_param)
            conn.commit()
        conn.close()
        print("FTSPLIT:数据写入完毕！")
    else:
        print("FTSPLIT:没有可写入的数据！")

    # ========== 配股信息 ============ #
    df_pg = pd.DataFrame()
    print("FTSPLIT:正在查找配股信息...")
    times_retry = 3
    while df_pg.empty ==True and times_retry!=0:
        df_pg = split_pg(proxy=0)
        times_retry = times_retry-1
    df_pg['除权日']=df_pg['除权日'].astype('datetime64')
    df_pg = df_pg[df_pg['除权日']==today]
    if df_pg.empty !=True:
        df_pg = df_pg.reset_index(range(len(df_pg)), drop=True)
        for m in range(len(df_pg)):
            Date_pg = df_pg.get_value(m,'除权日')
            Code_pg = df_pg.get_value(m,'股票代码')
            bl_pg = df_pg.get_value(m,'配股比例（10配）')
            pgj_pg = df_pg.get_value(m,'配股价')
            sql_ftsplitupdate="INSERT IGNORE INTO `ftsplit`(`code`, `date`, `配股`, `配股价`) VALUES (%s,%s,%s,%s)"
            param=(Code_pg,Date_pg,bl_pg,pgj_pg)
            cur=conn.cursor()
            cur.execute(sql_ftsplitupdate,param)
            conn.commit()
        print("FTSPLIT:配股信息更新完毕!")
    else:
        print("FTSPLIT:没有可更新的配股信息!")
    return 1

if __name__ == '__main__' :
    ftsplit()