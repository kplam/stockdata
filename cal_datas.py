#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
from kpfunc.indicator import *
from numpy import isnan
import datetime
import pandas as pd
import numpy as np


class calc:
    def __init__(self,conn='local',length=365):
        print("CALC:正在获取数据...")
        self.con = localconn() if conn =='local' else serverconn()
        self.datelist = pd.read_sql("select distinct `date` from `indexdb` ORDER BY `date` DESC limit 0,2",self.con)['date'].values
        self.today,self.lastdate = self.datelist[0],self.datelist[1]
        self.date_start = self.today-datetime.timedelta(days=length)
        self.alldayline = pd.read_sql("select * from `dayline` WHERE `date` BETWEEN '%s'and '%s'" % (self.date_start, self.today), self.con)
        self.allsplit = pd.read_sql("select * from `ftsplit` WHERE `date` BETWEEN '%s'and '%s'ORDER BY `date` DESC " % (self.date_start, self.today), self.con)
        self.df_splite = self.allsplit[self.allsplit['date']==self.today].reset_index(drop=True)
        self.df_dayline = self.alldayline[self.alldayline['date']==self.today].reset_index(drop=True)
        self.df_dayline_lastdate = self.alldayline[self.alldayline['date']==self.lastdate].reset_index(drop=True)
        self.df_ipo = pd.read_sql("select `证券代码`,`首发日期`,`首发价格` from `basedata` WHERE `首发日期` ='%s'"%(self.today),self.con)

    def adjfactor(self):
        print("CALC:正在计算涨跌幅...")
        codelist = self.df_dayline['code'].values
        codelist_lastdate = self.df_dayline_lastdate['code'].values
        codelist_ftsplit = self.df_splite['code'].values
        codelist_ipo = self.df_ipo['证券代码'].values
        list =[]
        for code in codelist:
            if code in codelist_lastdate and code not in codelist_ftsplit:
                close = self.df_dayline[self.df_dayline['code']==code]['close'].values[0]
                preclose = self.df_dayline_lastdate[self.df_dayline_lastdate['code']==code]['close'].values[0]
                adjfactor = self.df_dayline_lastdate[self.df_dayline_lastdate['code']==code]['adjfactor'].values[0]
                adjcump =self.df_dayline_lastdate[self.df_dayline_lastdate['code']==code]['adjcump'].values[0]
                percentage = (close /preclose-1)*100
                list.append([code,self.today,close,preclose,adjfactor,adjcump,percentage])
            elif code in codelist_lastdate and code in codelist_ftsplit:
                close = self.df_dayline[self.df_dayline['code'] == code]['close'].values[0]
                preclose = self.df_dayline_lastdate[self.df_dayline_lastdate['code'] == code]['close'].values[0]
                ftd = self.df_splite[self.df_splite['code']==code]
                ds = ftd.get_value(0, '红股')
                rs = ftd.get_value(0, '配股')
                rsprice = ftd.get_value(0, '配股价')
                di = ftd.get_value(0, '红利')
                adj_preclose = (int(((preclose + rsprice * rs / 10 - di / 10) / (1 + rs / 10 + ds / 10))*100+0.5))/100
                adjfactor = preclose / adj_preclose
                adjcump = self.df_dayline_lastdate[self.df_dayline_lastdate['code'] == code]['adjcump'].values[0]*adjfactor
                percentage = (close / adj_preclose - 1) * 100
                list.append([code,self.today, close, preclose, adjfactor, adjcump, percentage])
                sql_updatesplit = "update `ftsplit` set `单次复权因子`='%s',`累计复权因子`='%s',`前收盘价`='%s',`除权价`='%s'" \
                                  " WHERE `code`='%s' and `date`='%s'"%(adjfactor,adjcump,preclose,adj_preclose,code,self.today)
                cur =self.con.cursor()
                cur.execute(sql_updatesplit)
                self.con.commit()
            else:
                if code in codelist_ipo:
                    close = self.df_dayline[self.df_dayline['code']==code]['close'].values[0]
                    ipoprice = self.df_ipo[self.df_ipo['证券代码']==code]['首发价格'].values[0]
                    preclose=ipoprice
                    percentage = (close / ipoprice - 1)*100
                    adjfactor = 1
                    adjcump = 1
                    list.append([code,self.today, close, preclose, adjfactor, adjcump, percentage])
                else:
                    sql_getdayline="select * from `dayline` WHERE `code`='%s' ORDER BY `date` DESC LIMIT 0,2"%(code)
                    df_dayline = pd.read_sql(sql_getdayline,self.con)
                    close = df_dayline.get_value(0,'close')
                    preclose = df_dayline.get_value(1,'close')
                    lastdate = df_dayline.get_value(1,'date')
                    sql_getftsplit = "select * from `ftsplit` WHERE `code`='%s' and `date`>'%s' ORDER BY `date` ASC "%(code,lastdate)
                    dfsplit =pd.read_sql(sql_getftsplit,self.con)
                    if dfsplit.empty == True:
                        percentage = (close /preclose-1)*100
                        adjfactor = df_dayline.get_value(1,'adjfactor')
                        adjcump = df_dayline.get_value(1,'adjcump')
                        list.append([code,self.today, close, preclose, adjfactor, adjcump, percentage])
                    else:
                        preclose2 = 1
                        adjcump2 = 1
                        for i in range(len(dfsplit)):
                            splitdate= dfsplit.get_value(i,'date')
                            ds = dfsplit.get_value(i, '红股')
                            rs = dfsplit.get_value(i, '配股')
                            rsprice = dfsplit.get_value(i, '配股价')
                            di = dfsplit.get_value(i, '红利')
                            adj_preclose = (int(
                                ((preclose + rsprice * rs / 10 - di / 10) / (1 + rs / 10 + ds / 10)) * 100 + 0.5)) / 100
                            if i==0:
                                adjfactor = preclose / adj_preclose
                                preclose2 =adj_preclose
                                adjcump = df_dayline[df_dayline['code'] == code]['adjcump'].values[1] * adjfactor
                                adjcump2 = adjcump
                                sql_updatesplit = "update `ftsplit` set `单次复权因子`='%s',`累计复权因子`='%s',`前收盘价`='%s',`除权价`='%s'" \
                                                  " WHERE `code`='%s' and `date`='%s'" % (
                                                  adjfactor, adjcump, preclose, adj_preclose, code, splitdate)
                                cur = self.con.cursor()
                                cur.execute(sql_updatesplit)
                                self.con.commit()
                            else:
                                adjfactor = preclose2 / adj_preclose
                                preclose2 = adj_preclose
                                adjcump = adjcump2 * adjfactor
                                adjcump2 = adjcump
                                sql_updatesplit = "update `ftsplit` set `单次复权因子`='%s',`累计复权因子`='%s',`前收盘价`='%s',`除权价`='%s'" \
                                                  " WHERE `code`='%s' and `date`='%s'" % (
                                                      adjfactor, adjcump, preclose2, adj_preclose, code, splitdate)
                                cur = self.con.cursor()
                                cur.execute(sql_updatesplit)
                                self.con.commit()
                        percentage = (close/preclose2-1)*100
                        list.append([code, self.today, close, preclose, preclose/preclose2, adjcump, percentage])

        sql_turncate ="TRUNCATE `dayline_tmp`"
        cur = self.con.cursor()
        cur.execute(sql_turncate)
        self.con.commit()
        df_adj=pd.DataFrame(list,columns=['code', 'date', 'close', 'preclose', 'adjfactor', 'adjcump', 'percentage'])
        df_adj_update = df_adj[['code', 'date', 'adjfactor', 'adjcump']]
        df_adj_update.to_sql('dayline_tmp',con=self.con,flavor='mysql',schema='stockdata',if_exists='append',index=False,dtype=None)
        return df_adj

    def tamodel(self):
        print("CALC:正在计算技术分析模型...")
        List_TA_Result=[]
        sql_updatedayline = "select * from `dayline` WHERE `date`='%s'"%(self.today)
        sql_updateftsplit = "select * from `ftsplit` WHERE `date`='%s'"%(self.today)
        df_updatedayline = pd.read_sql(sql_updatedayline,self.con)
        df_updateftsplit = pd.read_sql(sql_updateftsplit,self.con)
        self.alldayline = pd.concat((self.alldayline[self.alldayline['date']<self.today],df_updatedayline),ignore_index=True)
        self.allsplit = pd.concat((self.allsplit[self.allsplit['date']<self.today],df_updateftsplit),ignore_index=True)

        for i in range(len(self.df_dayline)):
            symbol = self.df_dayline.get_value(i,'code')
            # =============== get data ==================#
            df_pre = self.alldayline[self.alldayline['code']==symbol].reset_index(drop=True)
            df_split = self.allsplit[self.allsplit['code']==symbol].reset_index(drop=True)
            if len(df_pre) > 80:
                # ============= adjfactor =================#
                if df_split.empty == True:
                    df = df_pre
                else:
                    adjcump = df_pre.get_value(len(df_pre) - 1, 'adjcump')
                    List_pre = []
                    for j in range(len(df_pre)):
                        high = df_pre.get_value(j, 'high') / (adjcump / df_pre.get_value(j, 'adjcump'))
                        open = df_pre.get_value(j, 'open') / (adjcump / df_pre.get_value(j, 'adjcump'))
                        low = df_pre.get_value(j, 'low') / (adjcump / df_pre.get_value(j, 'adjcump'))
                        close = df_pre.get_value(j, 'close') / (adjcump / df_pre.get_value(j, 'adjcump'))
                        vol = df_pre.get_value(j, 'vol')
                        date = df_pre.get_value(j, 'date')
                        for k in range(len(df_split)):
                            date_split = df_split.get_value(k, 'date')
                            split = df_split.get_value(k, '红股')
                            if date < date_split:
                                vol = vol * (1 + split / 10)
                            else:
                                vol = vol * 1
                        List_pre.append((symbol, date, high, open, low, close, vol, df_pre.get_value(j, 'amo'),
                                         df_pre.get_value(j, 'adjfactor'), df_pre.get_value(j, 'adjcump')))
                    df = pd.DataFrame(List_pre, columns=['code', 'date', 'high', 'open', 'low', 'close', 'vol', 'amo',
                                                         'adjfactor', 'adjcump'])
                # ============== prepare data to calculate ==============#
                dayline_high = df['high'].values
                dayline_open = df['open'].values
                dayline_low = df['low'].values
                dayline_close = df['close'].values
                dayline_vol = df['vol'].values
                dayline_amo = df['amo'].values

                # ===============indicator calculate======================#
                df['jll'], df['jlh'] = jl(dayline_open, dayline_close, dayline_high, dayline_low,dayline_amo)
                df['js'] = js(dayline_open, dayline_close, dayline_high, dayline_low, dayline_amo)
                df['kprsi'] = kprsi(dayline_close)
                df = df[len(df) - 2:]
                df = df.reset_index(drop=True)

                # ================ result to csv =========================#
                for j in range(len(df)):
                    if j > 0 and isnan(df.get_value(j, 'jlh')) != True:
                        close_cp = df.get_value(j, 'close')
                        close_cp_ref = df.get_value(j - 1, 'close')
                        jshort_cp = df.get_value(j, 'js')
                        jlh_cp = df.get_value(j, 'jlh')
                        kprsi_cp = df.get_value(j, 'kprsi')
                        if close_cp_ref < jshort_cp and close_cp > jshort_cp and close_cp > jlh_cp and close_cp > kprsi_cp:
                            List_TA_Result.append(symbol)


                # ========= error output ============ #
        return List_TA_Result

    def amorank(self):
        df_data = self.df_dayline
        df_data = df_data.sort_values(by=['amo'], ascending=False)
        df_data['AmoRank'] = pd.Series(np.arange(len(df_data['date'])) + 1, index=df_data.index)
        df_data = df_data[['code', 'date', 'AmoRank']]
        df_data = df_data.reset_index(drop=True)
        result = []
        df_list = calc.adjfactor(self)
        taresultlist = calc.tamodel(self)
        # print(taresultlist)
        print("CALC:正在按成交额进行排序...")
        for i in range(len(df_data)):
            code = df_data.get_value(i, 'code')
            date = df_data.get_value(i, 'date')
            fAmorank = df_data.get_value(i, 'AmoRank')
            sql_refar = "select `AmoRank` from `usefuldata` WHERE `code` ='%s' and `date`<'%s' and `AmoRank` is NOT NULL" \
                        " ORDER BY `date` DESC LIMIT 0,1" % (code, date)
            df_refar = pd.read_sql(sql_refar, self.con)
            if df_refar.empty == False:
                ref_ar = df_refar.values[0][0]
                ARaise = fAmorank - ref_ar
            else:
                ARaise = np.nan
            percentage = df_list[df_list['code']==code]['percentage'].values[0]
            taresult = '1' if code in taresultlist else '0'
            result.append([code, date, fAmorank, ARaise,percentage,taresult])
        result=pd.DataFrame(result,columns=['code','date','AmoRank','ARaise','precentage','taresult'])
        print("CALC:正在将成交量信息写入数据库...")
        errorlist = []
        try:
            result.to_sql('usefuldata',self.con,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
        except Exception as e:
            errorlist.append(e)
        dferrorlist = pd.DataFrame(errorlist)
        dferrorlist.to_csv(path()+'/error/amorank.csv')
        return result

if __name__=='__main__':
    t = datetime.datetime.today()
    print(t)
    c=calc()
    c.amorank()
    t = datetime.datetime.today()-t
    print(t)