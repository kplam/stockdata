#!C:\Users\KPLAM\AppData\Local\Programs\Python\Python36\python.exe
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from kpfunc.getdata import *
from kpfunc.function import *
import datetime,math,json
from cal_financial import cal_financial

def get_usefuldata(**kwargs):
    """
    :param kwargs:{date='str'(default LastTradeDay), code='str', amorank='int', araise='int',focus=Fault/True/None(default)}
    :return:pandas.DataFrame
    """
    conn = localconn()
    # sql_ld ="select `date` from `usefuldata` ORDER by `date` DESC limit 1"
    # lastdate = pd.read_sql(sql_ld,conn)['date'][0]
    lastdate = datetime.date.today()
    sWhere = " WHERE 1 "
    if len(kwargs)==0:
        sWhere = sWhere + "and `date` = '%s'" % (str(lastdate))
    else:
        if 'code' in kwargs:
            sCode = kwargs['code']
            if re.match("\d{6}",sCode):
                sWhere = sWhere + " and `code`='%s'"%(sCode)
            else:
                raise Exception("Error Param!")
        elif 'date' in kwargs:
            sDate = kwargs['date']
            if is_valid_date(sDate):
                sWhere = sWhere + "and `date` = '%s'" % (sDate)
            else:
                raise Exception("Error Param!")
        elif 'date' in kwargs and 'code' in kwargs:
            sCode = kwargs['code']
            sDate = kwargs['date']
            if re.match("\d{6}", sCode):
                sWhere = sWhere + " and `code`='%s'" % (sCode)
            else:
                raise Exception("Error Param!")
            if is_valid_date(sDate):
                sWhere = sWhere + "and `date` >= '%s'" % (sDate)
            else:
                raise Exception("Error Param!")
        else:
            pass

        if 'amorank' in kwargs:
            amorankparam = kwargs['amorank']
            if re.match("^[-+]?\d+(\.\d+)?$", amorankparam):
                sWhere = sWhere + " and `AmoRank`<'%s'" % (amorankparam)
            else:
                raise Exception("Error Param!")

        if 'araise' in kwargs:
            araiseparam = kwargs['araise']
            if re.match("^[-+]?\d+(\.\d+)?$", araiseparam):
                sWhere = sWhere + " and `ARaise`<'%s'" % (araiseparam)
            else:
                raise Exception("Error Param!")

        if 'focus' in kwargs:
            bFocus = kwargs['focus']
            if bFocus == 'True':
                sWhere = sWhere + " and `涨跌动因`!=''"
            elif bFocus == 'False':
                sWhere = sWhere + " and `涨跌动因` =''"
            elif bFocus == 'None':
                sWhere = sWhere
            else:
                raise Exception("Error Param!")
    sql_query = "select * from `usefuldata`"
    sql_query =sql_query + sWhere
    df = pd.read_sql(sql_query,localconn())
    table =df.values

    if 'amorank' not in kwargs and 'araise' not in kwargs:
        if 'code' not in kwargs:
            list_default=[]
            for elem in table:
                code,date,amorank,araise,percentage,focus,taresult=elem
                araisecompare  = -1/max(math.log((amorank-araise),math.e),1)*1.25*(amorank-araise)
                if amorank<len(table)//6 and araise<araisecompare:
                    list_default.append([code,date,amorank,araise,percentage,focus,taresult,araisecompare])
            df=pd.DataFrame(list_default,columns=['code','date','amorank','araise','percentage','focus','taresult','araisecompare'])

        elif 'code' in kwargs:
            list_default=[]
            sql_nums_on_trade = "SELECT `date`,`ontrade` FROM statistics"
            df_nums_on_trade = pd.read_sql(sql_nums_on_trade,conn)
            df2 = pd.merge(df,df_nums_on_trade)
            df2.to_csv('df2.csv')
            for elem in df2.values:
                code,date,amorank,araise,percentage,focus,taresult,nums_on_trade=elem
                araisecompare  = -1/max(math.log((amorank-araise),math.e),1)*1.25*(amorank-araise)
                amorankcompare = nums_on_trade//6
                if amorank<amorankcompare and araise<araisecompare:
                    list_default.append([code,date,amorank,araise,percentage,focus,taresult,araisecompare,amorankcompare])
            df=pd.DataFrame(list_default,columns=['code','date','amorank','araise','percentage','focus','taresult','araisecompare','amorankcompare'])
        else:
            df=pd.DataFrame(columns=['code','date','amorank','araise','percentage','focus','taresult','araisecompare','amorankcompare'])
    if df.empty != True:
        df = df[['code','date','amorank','araise','percentage','focus']]
        df['date']=df['date'].astype('str')
    else:
        df=pd.DataFrame()
    return df

def tech_analysis(sModel='1',**kwargs):
    conn = localconn()
    try:
        if 'code' in kwargs:
            sCode=kwargs['code']
            sql_indicator ="Select `date` from `usefuldata` WHERE `code`='%s' and `taresult` LIKE '%%%s%%'" % (sCode, sModel)
            DF_indicator = pd.read_sql(sql_indicator, conn)
            DF_indicator['date'] = DF_indicator['date'].astype('str')
            taoutput = DF_indicator.to_json(orient='records', force_ascii=False)
            taoutput = json.loads(taoutput)
        elif 'date' in kwargs:
            sDate = kwargs['date']
            sql_indicator = "Select `code` from `usefuldata` where `date`='%s' and `taresult` LIKE '%%%s%%'" % (sDate, sModel)
            DF_indicator = pd.read_sql(sql_indicator, conn)
            taoutput = DF_indicator.to_json(orient='records', force_ascii=False)
            taoutput = json.loads(taoutput)
        else:
            taoutput={"message":"error!"}
        return taoutput
    except:
        return {"message":"error!"}

def tdxblock(num=1):
    for N in range(num):
        try:
            today = str(datetime.date.today() - datetime.timedelta(days=N))
            cf = cal_financial(localconn()).median()
            ta_js = tech_analysis(sModel='1', date=today)
            ta = [elem['code'] for elem in ta_js]
            ud = get_usefuldata(date=today)['code'].values
            result = list(set(cf).intersection(set(ta)).intersection(set(ud)))

            path = r"D:\Qouting Software\new_pttq_v9\T0002\blocknew\%s.blk" % (today[8:10])
            f = open(path, 'w+')

            for i in range(len(result)):
                symbol = result[i]
                if symbol[0] == '6':
                    f.write('1' + symbol + '\n')
                else:
                    f.write('0' + symbol + '\n')
            f.close()
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    tdxblock(30)







