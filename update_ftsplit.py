#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
import re
import datetime
from kpfunc.getdata import *
from kpfunc.spyder import myspyder

def split_sz(Quarter,iLong,proxy=0,conn=localconn()): # 送转
    sztable = []
    List_Fin_SZ = []
    sz_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=SZBL&fd=%s&st=2&sr=true&p=1&ps=%s'%(Quarter,iLong)
    get_url= "error!"
    times_retry = 10
    while get_url == "error!" and times_retry != 0:
        get_url = myspyder(sz_url,proxy)
        times_retry = times_retry -1
    if get_url != "error!":
        try:
            return_list = re.findall("\"(.*?)\"", get_url.text)
            for j in range(len(return_list)):
                appd = re.split(",", return_list[j])
                sztable.append(appd)

            szlist = pd.DataFrame(sztable, columns=['股票代码', '股票简称', '利润分配', '送转比例', '现金分红', '每股收益(元)',
                                                    '每股未分配利润(元)', '每股未分配利润(元)', '上期每股未分配利润(元)',
                                                    '上期每股资本公积金(元)', '股权登记日', '公告日期', '财报'])
            szlist = szlist[['股票代码', '送转比例', '现金分红', '股权登记日']]

            for k in range(len(szlist)):
                symbol = szlist.get_value(k, '股票代码')
                bookindate = szlist.get_value(k, '股权登记日')
                if bookindate != '':
                    sqli = "SELECT * FROM `dayline` WHERE `date` > '%s' ORDER BY `date` ASC Limit 0,1" % (bookindate)
                    checkdate = pd.read_sql(sqli,conn)
                    if checkdate.empty == False:
                        split_date = checkdate.get_value(0, 'date')
                        sz = szlist.get_value(k, '送转比例')
                        xj = szlist.get_value(k, '现金分红')
                        sz_spl = re.split(u"([\u4e00-\u9fff]+)", sz)
                        xj_spl = re.split(u"([\u4e00-\u9fff]+)", xj)
                        sz_calA = float(sz_spl[2])
                        if len(sz_spl) > 1:
                            if len(sz_spl) > 4:
                                sz_calB = float(sz_spl[4])
                            else:
                                sz_calB = 0
                            sz_cal = sz_calA + sz_calB
                        else:
                            sz_cal = 0
                        if len(xj_spl) > 2:
                            xj_cal = float(xj_spl[2])
                        else:
                            xj_cal = 0
                        List_Fin_SZ.append([symbol, sz_cal, xj_cal, split_date])
        except:
            pass
    List_Fin_SZ = pd.DataFrame(List_Fin_SZ, columns=['symbol', 'sz_cal', 'xj_cal', 'date'])
    return List_Fin_SZ

def split_xj(Quarter,iLong,proxy=0,conn=localconn()): # 现金分红
    xj_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=FHBL&fd=%s&st=2&sr=true&p=1&ps=%s'%(Quarter,iLong)
    get_url = "error!"
    times_retry = 10
    xjtable = []
    List_Fin_xj = []
    while get_url == "error!" and times_retry != 0:
        get_url = myspyder(xj_url, proxy)
        times_retry = times_retry - 1
    if get_url != "error!":
        try:
            return_list = re.findall("\"(.*?)\"",get_url.text)
            # print(return_list)
            for j in range(len(return_list)):
                appd = re.split(",",return_list[j])
                xjtable.append(appd)

            xjlist = pd.DataFrame(xjtable, columns=['股票代码','股票简称','利润分配','送转比例','现金分红','现金分红总额(万元)',
                                                  '分红比例（10送）','股息率','每股收益(元)','每股未分配利润(元)',
                                                  '上期每股未分配利润(元)','股权登记日','公告日','财报'])
            xjlist = xjlist[['股票代码','送转比例','分红比例（10送）','股权登记日']]
            for k in range(len(xjlist)):
                symbol = xjlist.get_value(k,'股票代码')
                bookindate =xjlist.get_value(k,'股权登记日')
                if bookindate !='':
                    sqli= "SELECT * FROM `dayline` WHERE `date` > '%s' ORDER BY `date` ASC Limit 0,1" % (bookindate)
                    checkdate =pd.read_sql(sqli,conn)
                    if checkdate.empty == False:
                        split_date = checkdate.get_value(0,'date')
                        sz = xjlist.get_value(k,'送转比例')
                        xj = xjlist.get_value(k,'分红比例（10送）')
                        sz_spl = re.split(u"([\u4e00-\u9fff]+)" ,sz)
                        xj_spl = re.split(u"([\u4e00-\u9fff]+)" ,xj)

                        if len(sz_spl)>1:
                            sz_calA = float(sz_spl[2])
                            if len(sz_spl)>4:
                                sz_calB = float(sz_spl[4])
                            else:
                                sz_calB = 0
                            sz_cal = sz_calA+sz_calB
                        else:
                            sz_cal = 0
                        xj_cal = float(xj_spl[0])
                        List_Fin_xj.append((symbol,sz_cal,xj_cal,split_date))
        except:
            pass
    List_Fin_xj = pd.DataFrame(List_Fin_xj,columns=['symbol','sz_cal','xj_cal','date'])
    return List_Fin_xj

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

            print("配股信息查找完毕，正在写入数据库！")
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
    print("今天是",today,".")
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
        print("正在获取分红数据...")
        for Quarter in List_Quarter:
            df_Fin_SZ = split_sz(Quarter=Quarter,iLong=iLong,proxy=0,conn=conn)
            df_Fin_xj = split_xj(Quarter=Quarter,iLong=iLong,proxy=0,conn=conn)
            df_Fin = pd.concat((df_Fin_SZ, df_Fin_xj)).sort_values('date', ascending=False).drop_duplicates()
            df_ftsplit = pd.concat((df_ftsplit,df_Fin))
        df_ftsplit = pd.DataFrame(np.array(df_ftsplit),columns=['code','红股','红利','date'])
        times_retry = times_retry-1

    df_sqlupdate = df_ftsplit[df_ftsplit['date']==today]

    if df_sqlupdate.empty != True:
        df_sqlupdate = df_sqlupdate.reset_index(range(len(df_sqlupdate)), drop=True)
        for i in range(len(df_sqlupdate)):
            code = str(df_sqlupdate.get_value(i,'code'))
            sz = float(df_sqlupdate.get_value(i,'红股'))
            xj = float(df_sqlupdate.get_value(i,'红利'))
            sdate = str(df_sqlupdate.get_value(i,'date'))
            sql_param=(code,sz,xj,sdate)
            sql_update = "INSERT IGNORE INTO `ftsplit`(`code`, `红股`, `红利`,`date`) VALUES (%s,%s,%s,%s)"
            cur = conn.cursor()
            cur.execute(sql_update,sql_param)
            conn.commit()
        conn.close()
        print("数据写入完毕！")
    else:
        print("没有可写入的数据！")

    # ========== 配股信息 ============ #
    df_pg = pd.DataFrame()
    print("正在查找配股信息...")
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
            sql_ftsplitupdate="INSERT IGNORE INTO `ftsplit`(`code`, `date`, `配股`, `配股价`) VALUES ('%s','%s','%s','%s')"%(Code_pg,Date_pg,bl_pg,pgj_pg)
            cur=conn.cursor()
            cur.execute(sql_ftsplitupdate)
            conn.commit()
        conn.close()
        print("配股信息更新完毕!")
    else:
        print("没有可更新的配股信息!")
    return 1

if __name__ == "__main__":
    ftsplit()