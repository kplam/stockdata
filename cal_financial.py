#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-01
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
import pandas as pd
import datetime

class cal_financial:
    def __init__(self,conn = localconn()):
        """
        :param conn: set sql conn (localconn()/serverconn())
        """
        self.conn = conn
        sql_reportdate = "select distinct `报表日期` from faresult ORDER BY `报表日期` DESC"
        self.list_reportdate = pd.read_sql(sql_reportdate, self.conn)

    def updatesql(self):
        """
        updatesql before use other function
        :return:
        """
        df_result = pd.DataFrame()
        sql_quarter = "SELECT DISTINCT `报表日期` FROM `financial` ORDER BY `报表日期` DESC "
        Quarter = pd.read_sql(sql_quarter, self.conn)['报表日期'].astype('str')
        Quarter = Quarter.values
        for q in Quarter:
            print(q)
            sqli = "SELECT * FROM `financial` WHERE `报表日期` ='%s'"%(q)
            df = pd.read_sql(sqli,self.conn)
            df_tmp = df[(df['主营业务收入增长率'] > df['主营业务收入增长率'].median()) &
                     (df['净利润增长率'] > df['净利润增长率'].median()) &
                     (df['净资产增长率'] > df['净资产增长率'].median()) &
                     (df['三年平均净资收益率'] > df['三年平均净资收益率'].median()) &
                     ((df['每股资本公积金']+df['每股未分配利润']) > 2) &
                     (df['每股净资产']>1)
                     ]
            df_result = pd.concat([df_result,df_tmp])
        df_result = df_result[['代码','报表日期']]
        df_result.to_sql('faresult', con=self.conn, flavor='mysql', if_exists='replace',index=False, dtype=None)
        return print("Done!")

    def median(self,fWeight=0.8,iQuarter=12,fCompare=0.4):
        """
        :param fWeight: 权重衰减值，默认0.8
        :param iQuarter: 计算财务数量，默认最近12季
        :param fCompare: 加权对比值，权重值之和*fCompare,默认0.4
        :return: code list
        """
        list_reportdate = self.list_reportdate
        sReportdate = str(list_reportdate.get_value(iQuarter, '报表日期'))
        weight = []
        for i in range(len(list_reportdate)):
            reportdate = list_reportdate.get_value(i, '报表日期')
            weight.append((reportdate, 1 * fWeight ** i))
        weight = pd.DataFrame(weight, columns=['报表日期', 'weight'])
        weight = weight[:iQuarter]
        sql_FA = "Select * from `faresult` WHERE `报表日期`>'%s' ORDER BY `报表日期` DESC "%(sReportdate)
        DF_FA = pd.read_sql(sql_FA, self.conn)
        fa_result = pd.merge(DF_FA, weight)
        fa_result = fa_result['weight'].groupby(fa_result['代码']).sum()
        fa_result = fa_result.reset_index().sort_values(by=['weight'], ascending=False)
        list_FA = fa_result[fa_result.weight > weight['weight'].sum() * fCompare]['代码'].values
        return list_FA

    def gsz(self,iQuarter=0,crps=1,reps=1,npgr=20,cp=30,cap=30000):
        """
        :param iQuarter: 0 为最新季报，1为对上一季，如此类推
        :param crps: 每股资本公积>1(默认)
        :param reps: 每股未分配利润>1(默认)
        :param npgr: 净利润增长率>20(默认)
        :param cp: 现价>30(默认)
        :param cap:总股本<30000万
        :return: code list
        """
        list_reportdate = self.list_reportdate
        sReportdate = str(list_reportdate.get_value(iQuarter, '报表日期'))
        sql_FA = "Select * from `financial` WHERE `报表日期`='%s' and `每股资本公积金`>'%s' and `每股未分配利润`>'%s' and " \
                 "`净利润增长率`>'%s'"%(sReportdate, crps, reps, npgr)
        DF_FA = pd.read_sql(sql_FA, self.conn)
        result = []
        for i in range(len(DF_FA)):
            code=DF_FA.get_value(i,'代码')
            sql_ipo ="select `首发日期` from `basedata` WHERE `证券代码`='%s'"%(code)
            ipodate = pd.read_sql(sql_ipo, self.conn)

            ipodate=ipodate.values[0][0] if ipodate.empty == False else datetime.date.today()+datetime.timedelta(days=1)
            if datetime.date.today() - ipodate < datetime.timedelta(365*3):
                sql_close="select `close` from `dayline` WHERE `code`='%s' ORDER by `date` DESC limit 0,1"%(code)
                close=pd.read_sql(sql_close, self.conn)
                close =close.values[0][0] if close.empty == False else 0
                if close >cp :
                    sql_capital ="SELECT `总股本` FROM `capitalchange` WHERE `﻿股票代码` ='%s' ORDER BY `变动日期` DESC " \
                                 "limit 0,1"%(code)
                    capital= pd.read_sql(sql_capital, self.conn).values[0][0]
                    if capital<cap:
                        date_split=str(datetime.date.today()-datetime.timedelta(days=180))
                        sql_split="select `红股` from `ftsplit` WHERE `code`='%s' and `date`>'%s'"%(code,date_split)
                        split=pd.read_sql(sql_split,self.conn)
                        if split.empty == True:
                            result.append(code)
                        else:
                            if split.values[0][0] == 0:
                                result.append(code)
        return result

    def custom(self,sfield,swhere):
        """
        get param from url
        :param sfield:
        :param swhere:
        :return: json
        """
        sql_custom = "select " + sfield + " from `financial` where " + swhere
        df_custom = pd.read_sql(sql_custom,self.conn)
        df_custom['报表日期']=df_custom['报表日期'].astype('str')
        json_output = df_custom.to_json(orient='records',force_ascii=False)
        return json_output



if __name__ == "__main__" :
    # cal_financial(conn=localconn()).updatesql()
    # cal_financial(conn=serverconn()).updatesql()
    cal_financial(conn=localconn()).updatesql()
    # print(cal_financial(conn=localconn()).median())
