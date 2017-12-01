# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
import csv
import pandas as pd

def update_dzhconcept(ser):
    """
    :param ser: server,local or both
    :return:
    """
    Errorlist=[]
    sqli = "UPDATE `basedata` SET `所属主题` = %s, `所属概念` = %s WHERE `basedata`.`证券代码` = %s ;"
    with open(path()+"/data/dzhconcept/concept.csv",encoding='gb18030') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            try:
                print(row['证券代码'],row['证券简称'],row['所属概念'])
                if ser =="server":
                    conn = serverconn()
                    cur = conn.cursor()
                    cur.execute(sqli, (row['所属主题'], row['所属概念'], row['证券代码']))
                    conn.commit()
                elif ser =="local":
                    conn = localconn()
                    cur = conn.cursor()
                    cur.execute(sqli, (row['所属主题'], row['所属概念'], row['证券代码']))
                    conn.commit()
                else:
                    conn1 = serverconn()
                    cur = conn1.cursor()
                    cur.execute(sqli, (row['所属主题'], row['所属概念'], row['证券代码']))
                    conn1.commit()
                    conn2 = localconn()
                    cur = conn2.cursor()
                    cur.execute(sqli, (row['所属主题'], row['所属概念'], row['证券代码']))
                    conn2.commit()
            except Exception as e:
                print(row['证券代码'],e)
                Errorlist.append((row['证券代码'],e))
    f.close()
    return Errorlist
def update_dzhcontrol(ser):
    """
    :param ser: server,local or both
    :return:
    """
    Errorlist = []
    sqli = "UPDATE `basedata` SET `实际控制人名称` = %s, `实际控制人类型` = %s,`央企控制人名称`=%s,`控股股东名称`=%s,`控股股东类型`=%s WHERE `basedata`.`证券代码` = %s ;"
    with open(path() + "/data/dzhcontrol/control.csv", encoding='gb18030') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            try:
                print(row['证券代码'], row['实际控制人名称'], row['实际控制人类型'],row['央企控制人名称'],row['控股股东名称'],row['控股股东类型'])
                if ser == "server":
                    conn = serverconn()
                    cur = conn.cursor()
                    cur.execute(sqli, (row['实际控制人名称'], row['实际控制人类型'],row['央企控制人名称'],row['控股股东名称'],row['控股股东类型'],row['证券代码']))
                    conn.commit()
                elif ser == "local":
                    conn = localconn()
                    cur = conn.cursor()
                    cur.execute(sqli,  (row['实际控制人名称'], row['实际控制人类型'],row['央企控制人名称'],row['控股股东名称'],row['控股股东类型'],row['证券代码']))
                    conn.commit()
                else:
                    conn1 = serverconn()
                    cur = conn1.cursor()
                    cur.execute(sqli, (row['实际控制人名称'], row['实际控制人类型'],row['央企控制人名称'],row['控股股东名称'],row['控股股东类型'],row['证券代码']))
                    conn1.commit()
                    conn2 = localconn()
                    cur = conn2.cursor()
                    cur.execute(sqli, (row['实际控制人名称'], row['实际控制人类型'],row['央企控制人名称'],row['控股股东名称'],row['控股股东类型'],row['证券代码']))
                    conn2.commit()
            except Exception as e:
                print(row['证券代码'], e)
                Errorlist.append((row['证券代码'], e))
    f.close()
    return Errorlist
def update_capitalchange(ser):
    """
    :param ser: server,local or both
    :return:
    """
    Errorlist = []
    sqli = "INSERT IGNORE INTO `capitalchange`(`﻿股票代码`, `变动日期`, `变动原因`, `总股本_变动`, `流通A股_变动`, " \
           "`流通B股_变动`, `总股本_前值`, `流通A股_前值`, `流通B股_前值`, `总股本`, `流通A股`, `流通B股`) VALUES " \
           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    with open(path() + "/data/dzhcapitalchange/capitalchange.csv", encoding='utf-8') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            try:
                param = (row['﻿股票代码'], row['变动日期'],row['变动原因'],row['总股本_变动'],row['流通A股_变动'],
                         row['流通B股_变动'],row['总股本_前值'], row['流通A股_前值'], row['流通B股_前值'], row['总股本'],
                         row['流通A股'],  row['流通B股'])
                print(param)
                if ser == "server":
                    conn = serverconn()
                    cur = conn.cursor()
                    cur.execute(sqli, param)
                    conn.commit()
                elif ser == "local":
                    conn = localconn()
                    cur = conn.cursor()
                    cur.execute(sqli,param)
                    conn.commit()
                else:
                    conn1 = serverconn()
                    cur = conn1.cursor()
                    cur.execute(sqli,param)
                    conn1.commit()
                    conn2 = localconn()
                    cur = conn2.cursor()
                    cur.execute(sqli, param)
                    conn2.commit()
            except Exception as e:
                print(row['﻿股票代码'], e)
                Errorlist.append((row['﻿股票代码'], e))
    f.close()
    return Errorlist
if __name__=="__main__":
   concept_errorlist = update_dzhconcept(ser='both') # 注意导出数据是否完整 文件编码
   dfErrorList = pd.DataFrame( concept_errorlist)
   dfErrorList.to_csv(path() + '/error/dzhconcept.csv')
   print(dfErrorList)
   control_errorlist = update_dzhcontrol(ser='both') # 注意导出数据是否完整 文件编码
   dfErrorList2 = pd.DataFrame( control_errorlist)
   dfErrorList2.to_csv(path() + '/error/dzhcontrol.csv')
   print(dfErrorList2)
   capitalchange_errorlist = update_capitalchange(ser='both') # 改抬头，删字段，数字格式，文件编码utf-8
   dfErrorList3 = pd.DataFrame(capitalchange_errorlist)
   dfErrorList3.to_csv(path() + '/error/capitalchange.csv')
   print(dfErrorList3)
