#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:20:00 2017
"
@author: kplam
"""
from kpfunc.getdata import *
from kpfunc.function import path
from kpfunc.indicator import *
from numpy import isnan
import datetime
import pandas as pd
import numpy as np
from tenacity import retry,stop_after_attempt


class calc:
    def __init__(self,length=365):
        print("CALC:正在获取数据...")

        self.con = conn()

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
                ds = ftd['红股'][0]
                rs = ftd['配股'][0]
                rsprice = ftd['配股价'][0]
                di = ftd['红利'][0]
                adj_preclose = (int(((preclose + rsprice * rs / 10 - di / 10) / (1 + rs / 10 + ds / 10))*100+0.5))/100
                adjfactor = preclose / adj_preclose
                adjcump = self.df_dayline_lastdate[self.df_dayline_lastdate['code'] == code]['adjcump'].values[0]*adjfactor
                percentage = (close / adj_preclose - 1) * 100
                list.append([code,self.today, close, preclose, adjfactor, adjcump, percentage])
                sql_updatesplit = "update `ftsplit` set `单次复权因子`='%s',`累计复权因子`='%s',`前收盘价`='%s',`除权价`='%s'" \
                                  " WHERE `code`='%s' and `date`='%s'"%(adjfactor,adjcump,preclose,adj_preclose,code,self.today)

                self.con.execute(sql_updatesplit)
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
                    close = df_dayline['close'][0]
                    preclose = df_dayline['close'][1]
                    lastdate = df_dayline['date'][1]
                    sql_getftsplit = "select * from `ftsplit` WHERE `code`='%s' and `date`>'%s' ORDER BY `date` ASC "%(code,lastdate)
                    dfsplit =pd.read_sql(sql_getftsplit,self.con)
                    if dfsplit.empty == True:
                        percentage = (close /preclose-1)*100
                        adjfactor = df_dayline['adjfactor'][1]
                        adjcump = df_dayline['adjcump'][1]
                        list.append([code,self.today, close, preclose, adjfactor, adjcump, percentage])
                    else:
                        preclose2 = 1
                        adjcump2 = 1
                        for i in range(len(dfsplit)):
                            splitdate= dfsplit['date'][i]
                            ds = dfsplit['红股'][i]
                            rs = dfsplit['配股'][i]
                            rsprice = dfsplit['配股价'][i]
                            di = dfsplit['红利'][i]
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
                                self.con.execute(sql_updatesplit)

                                # cur = self.con.cursor()
                                # cur.execute(sql_updatesplit)
                                # self.con.commit()
                            else:
                                adjfactor = preclose2 / adj_preclose
                                preclose2 = adj_preclose
                                adjcump = adjcump2 * adjfactor
                                adjcump2 = adjcump
                                sql_updatesplit = "update `ftsplit` set `单次复权因子`='%s',`累计复权因子`='%s',`前收盘价`='%s',`除权价`='%s'" \
                                                  " WHERE `code`='%s' and `date`='%s'" % (
                                                      adjfactor, adjcump, preclose2, adj_preclose, code, splitdate)

                                self.con.execute(sql_updatesplit)

                                # cur = self.con.cursor()
                                # cur.execute(sql_updatesplit)
                                # self.con.commit()
                        percentage = (close/preclose2-1)*100
                        list.append([code, self.today, close, preclose, preclose/preclose2, adjcump, percentage])


        df_adj=pd.DataFrame(list,columns=['code', 'date', 'close', 'preclose', 'adjfactor', 'adjcump', 'percentage'])
        df_adj_update = df_adj[['code', 'date', 'adjfactor', 'adjcump']]
        sql_turncate ="TRUNCATE `dayline_tmp`"
        try:

            self.con.execute(sql_turncate)
            df_adj_update.to_sql('dayline_tmp', con=self.con, schema='stockdata', if_exists='append',
                                 index=False, dtype=None)
        except Exception as e:
            print(e)

        # cur = self.con.cursor()
        # cur.execute(sql_turncate)
        # self.con.commit()

        # df_adj_update.to_sql('dayline_tmp',con=self.con,flavor='mysql',schema='stockdata',if_exists='append',index=False,dtype=None)
        return df_adj

    def tamodel(self):
        print("CALC:正在计算技术分析模型...")
        List_TA_Result_1=[]
        List_TA_Result_2=[]
        sql_updatedayline = "select * from `dayline` WHERE `date`='%s'"%(self.today)
        sql_updateftsplit = "select * from `ftsplit` WHERE `date`='%s'"%(self.today)
        df_updatedayline = pd.read_sql(sql_updatedayline,self.con)
        df_updateftsplit = pd.read_sql(sql_updateftsplit,self.con)
        self.alldayline = pd.concat((self.alldayline[self.alldayline['date']<self.today],df_updatedayline),ignore_index=True)
        self.allsplit = pd.concat((self.allsplit[self.allsplit['date']<self.today],df_updateftsplit),ignore_index=True)

        for i in range(len(self.df_dayline)):
            symbol = self.df_dayline['code'][i]
            # =============== get data ==================#
            df_pre = self.alldayline[self.alldayline['code']==symbol].reset_index(drop=True)
            df_split = self.allsplit[self.allsplit['code']==symbol].reset_index(drop=True)
            if len(df_pre) > 80:
                # ============= adjfactor =================#
                if df_split.empty == True:
                    df = df_pre
                else:
                    adjcump = df_pre['adjcump'][len(df_pre) - 1]
                    List_pre = []
                    for j in range(len(df_pre)):
                        high = df_pre['high'][j] / (adjcump / df_pre['adjcump'][j])
                        open = df_pre['open'][j] / (adjcump / df_pre['adjcump'][j])
                        low = df_pre['low'][j] / (adjcump / df_pre['adjcump'][j])
                        close = df_pre['close'][j] / (adjcump / df_pre['adjcump'][j])
                        vol = df_pre['vol'][j]
                        date = df_pre['date'][j]
                        for k in range(len(df_split)):
                            date_split = df_split['date'][k]
                            split = df_split['红股'][k]
                            if date < date_split:
                                vol = vol * (1 + split / 10)
                            else:
                                vol = vol * 1
                        List_pre.append((symbol, date, high, open, low, close, vol, df_pre['amo'][j],
                                         df_pre['adjfactor'][j], df_pre['adjcump'][j]))
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
                if symbol in ['000002','000004','000001','600000']:
                    print(symbol)
                    print( df['kprsi'] )
                df['diff'],df['dea'], df['hist']=macd(dayline_close)
                df = df[len(df) - 2:]
                df = df.reset_index(drop=True)

                # ================ result to csv =========================#
                for j in range(len(df)):
                    if j > 0 and isnan(df['jlh'][j]) != True:
                        close_cp = df['close'][j]
                        close_cp_ref = df['close'][j-1]
                        jshort_cp = df['js'][j]
                        jlh_cp = df['jlh'][j]
                        kprsi_cp = df['kprsi'][j]
                        if close_cp_ref < jshort_cp and close_cp > jshort_cp and close_cp > jlh_cp and close_cp > kprsi_cp:
                            List_TA_Result_1.append(symbol)
                    if j>0 and isnan(df['hist'][j]) != True:
                        diff = df['diff'][j]
                        dea = df['dea'][j]
                        diffref = df['diff'][j-1]
                        dearef = df['dea'][j-1]
                        if diff > 0 and diff >dea and diffref<dearef:
                            List_TA_Result_2.append(symbol)
                # ========= error output ============ #
        return List_TA_Result_1,List_TA_Result_2

    @retry(stop=stop_after_attempt(3))
    def amorank(self):
        df_data = self.df_dayline
        df_data = df_data.sort_values(by=['amo'], ascending=False)
        df_data['amorank'] = pd.Series(np.arange(len(df_data['date'])) + 1, index=df_data.index)
        df_data = df_data[['code', 'date', 'amorank']]
        df_data = df_data.reset_index(drop=True)
        result = []
        df_list = calc.adjfactor(self)
        taresultlist1,taresultlist2 = calc.tamodel(self)
        # print(taresultlist)
        print("CALC:正在按成交额进行排序...")
        for i in range(len(df_data)):
            code = df_data['code'][i]
            date = df_data['date'][i]
            fAmorank = df_data['amorank'][i]
            sql_refar = "select `amorank` from `usefuldata` WHERE `code` ='%s' and `date`<'%s' and `amorank` is NOT NULL" \
                        " ORDER BY `date` DESC LIMIT 0,1" % (code, date)
            df_refar = pd.read_sql(sql_refar, self.con)
            if df_refar.empty == False:
                ref_ar = df_refar.values[0][0]
                ARaise = fAmorank - ref_ar
            else:
                ARaise = np.nan
            percentage = df_list[df_list['code']==code]['percentage'].values[0]

            if code in taresultlist1 and code in taresultlist2:
                taresult = '1,2'
            elif code in taresultlist1 and code not in taresultlist2:
                taresult = '1'
            elif code in taresultlist2 and code not in taresultlist1:
                taresult = '2'
            else:
                taresult = '0'

           # taresult = '1,2' if code in taresultlist1  else '0'
            result.append([code, date, fAmorank, ARaise,percentage,taresult])
        result=pd.DataFrame(result,columns=['code','date','amorank','araise','percentage','taresult'])
        print("CALC:正在将成交量信息写入数据库...")
        errorlist = []
        try:
            result.to_sql('usefuldata',self.con,schema='stockdata',if_exists='append',
                          index=False,chunksize=10000)
        except Exception as e:
            print(e)
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