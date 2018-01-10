# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on 15:20:00 2017-11-22
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path,gbk_to_utf8
import csv
import pandas as pd

def update_dzhconcept(ser):
    """
    :param ser: server,local or both
    :return:
    """
    Errorlist=[]
    sqli = "UPDATE `basedata` SET `所属主题` = %s, `所属概念` = %s WHERE `basedata`.`证券代码` = %s ;"
    with open(path()+"/data/dzhdata/concept.csv",encoding='utf-8') as f:
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
    with open(path() + "/data/dzhdata/control.csv", encoding='utf-8') as f:
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
    sql_last = "select `变动日期` from `capitalchange` ORDER BY `变动日期` DESC  limit 1"
    lastdate = pd.read_sql(sql_last,localconn()).values[0][0]
    # print(lastdate)
    Errorlist = []
    sqli = "INSERT IGNORE INTO `capitalchange`(`﻿股票代码`, `变动日期`, `变动原因`, `总股本_变动`, `流通A股_变动`, " \
           "`流通B股_变动`, `总股本_前值`, `流通A股_前值`, `流通B股_前值`, `总股本`, `流通A股`, `流通B股`) VALUES " \
           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    table=pd.read_csv(path() + "/data/dzhdata/capitalchange.csv",dtype='object')
    table['变动日期']=pd.to_datetime(table['变动日期'])
    # print(table.dtypes)
    table = table[table['变动日期']>lastdate].values
    # print(table)
    # with open(path() + "/data/dzhdata/capitalchange.csv", encoding='utf-8') as f:
    #     f_csv = csv.DictReader(f)
    for elem in table:
        try:
            # param = (row['﻿股票代码'], row['变动日期'],row['变动原因'],row['总股本_变动'],row['流通A股_变动'],
            #          row['流通B股_变动'],row['总股本_前值'], row['流通A股_前值'], row['流通B股_前值'], row['总股本'],
            #          row['流通A股'],  row['流通B股'])
            # print(param)
            param = [str(elem[i]) for i in range(len(elem))]
            if ser == "server":
                conn = serverconn()
                cur = conn.cursor()
                cur.execute(sqli, tuple(param))
                conn.commit()
            elif ser == "local":
                conn = localconn()
                cur = conn.cursor()
                cur.execute(sqli,tuple(param))
                conn.commit()
            else:
                conn1 = serverconn()
                cur = conn1.cursor()
                cur.execute(sqli,tuple(param))
                conn1.commit()
                conn2 = localconn()
                cur = conn2.cursor()
                cur.execute(sqli, tuple(param))
                conn2.commit()
        except Exception as e:
            print(param[0], e)
            Errorlist.append((param[0], e))
    # f.close()
    return Errorlist
def update_buyback(ser):
    """
        :param ser: server,local or both
        :return:
        """
    sql_last = "select `董事会通过日` from `buyback` ORDER BY `董事会通过日` DESC  limit 1"
    lastdate = pd.read_sql(sql_last,localconn()).values[0][0]
    Errorlist = []
    # sqli="insert ignore into `buyback`(`证劵代码`, `方案进度`, `董事会通过日`, `股东大会通过日`, `国资委通过日`, " \
    #     "`证监会通过日`, `回购资金上限_CNY`, `回购价格上限_CNY`, `回购股份预计_万`, `占总股本`, `占实际流通股`, `股份种类`," \
    #     " `回购资金来源`, `回购股份方式`, `回购股份实施期限`, `备注`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    table = pd.read_csv(path() + "/data/dzhdata/buyback.csv", dtype='object')
    # print(table)
    table['董事会通过日'] = pd.to_datetime(table['董事会通过日'])
    # print(table.dtypes)
    table = table[table['董事会通过日'] > lastdate].values
    table =pd.DataFrame(table,columns=['证劵代码', '方案进度', '董事会通过日', '股东大会通过日', '国资委通过日', '证监会通过日', '回购资金上限_CNY', '回购价格上限_CNY', '回购股份预计_万', '占总股本', '占实际流通股', '股份种类','回购资金来源', '回购股份方式', '回购股份实施期限', '备注'])
    table['董事会通过日'] = pd.to_datetime(table['董事会通过日'])
    table['回购资金上限_CNY']=table['回购资金上限_CNY'].astype('float')
    table['回购价格上限_CNY']=table['回购价格上限_CNY'].astype('float')
    table['回购股份预计_万']=table['回购股份预计_万'].astype('float')
    table['占实际流通股']=table['占实际流通股'].astype('float')
    table['占总股本']=table['占总股本'].astype('float')

    print(table.dtypes)
    print(table)
    # with open(path() + "/data/dzhdata/buyback.csv", encoding='utf-8') as f:
    #     f_csv = csv.DictReader(f)
    if ser == "local" or ser == "both":
        table.to_sql('buyback',localconn(),flavor='mysql',schema='stockdata',index=False,if_exists='append')
    if ser == "server" or ser == "both":
        table.to_sql('buyback',serverconn(),flavor='mysql',schema='stockdata',index=False,if_exists='append')

    # for param in table:
    #     try:
    #         # param = (row['证劵代码'], row['方案进度'], row['董事会通过日'], row['股东大会通过日'], row['国资委通过日'],
    #         #          row['证监会通过日'], row['回购资金上限_CNY'], row['回购价格上限_CNY'], row['回购股份预计_万'],
    #         #          row['占总股本'], row['占实际流通股'],row['股份种类'],row['回购资金来源'],row['回购股份方式'],
    #         #          row['回购股份实施期限'],row['备注'])
    #         # param = [str(elem[i]) for i in range(len(elem))]
    #         if ser == "server":
    #             conn = serverconn()
    #             cur = conn.cursor()
    #             cur.execute(sqli,tuple(param))
    #             conn.commit()
    #         elif ser == "local":
    #             conn = localconn()
    #             cur = conn.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn.commit()
    #         else:
    #             conn1 = serverconn()
    #             cur = conn1.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn1.commit()
    #             conn2 = localconn()
    #             cur = conn2.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn2.commit()
    #     except Exception as e:
    #         print(param[0],e)
    #         Errorlist.append((param[0], e))
    # f.close()
    return Errorlist
def update_incentive(ser):
    """
    :param ser: server,local or both
    :return:
    """
    sql_last = "select `薪酬委员会预案公告日` from `incentive` ORDER BY `薪酬委员会预案公告日` DESC  limit 1"
    lastdate = pd.read_sql(sql_last,localconn()).values[0][0]
    Errorlist = []
    sqli = "INSERT IGNORE INTO `incentive`(`股票代码`, `本期计划制定年度`, `本期计划激励次数`, `方案进度`, `激励标的物`, " \
           "`标的股票来源`, `激励总数_万`, `激励总数占当时总股本的比例`, `计划授权授予股票价格`, `本期计划有效期_年`, " \
           "`股权激励授予条件说明`, `薪酬委员会预案公告日`, `董事会修订方案日`, `股东大会通过日`, `独立财务顾问`, `律师事务所`," \
           " `备注`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    table = pd.read_csv(path() + "/data/dzhdata/incentive.csv", dtype='object')
    # print(table)
    table['薪酬委员会预案公告日'] = pd.to_datetime(table['薪酬委员会预案公告日'])
    # print(table.dtypes)
    table = table[table['薪酬委员会预案公告日'] > lastdate]
    if ser == "local" or ser == "both":
        table.to_sql('incentive',localconn(),flavor='mysql',schema='stockdata',index=False,if_exists='append')
    if ser == "server" or ser == "both":
        table.to_sql('incentive',serverconn(),flavor='mysql',schema='stockdata',index=False,if_exists='append')
    # with open(path() + "/data/dzhdata/incentive.csv", encoding='utf-8') as f:
    #     f_csv = csv.DictReader(f)
    # for elem in table:
    #     try:
    #         # param = (row['﻿股票代码'], row['本期计划制定年度'], row['本期计划激励次数'], row['方案进度'], row['激励标的物'],
    #         #          row['标的股票来源'], row['激励总数_万'], row['激励总数占当时总股本的比例'], row['计划授权授予股票价格'],
    #         #          row['本期计划有效期_年'], row['股权激励授予条件说明'], row['薪酬委员会预案公告日'], row['董事会修订方案日'],
    #         #          row['股东大会通过日'], row['独立财务顾问'], row['律师事务所'], row['备注'])
    #         param = [str(elem[i]) for i in range(len(elem))]
    #
    #         if ser == "server":
    #             conn = serverconn()
    #             cur = conn.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn.commit()
    #         elif ser == "local":
    #             conn = localconn()
    #             cur = conn.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn.commit()
    #         else:
    #             conn1 = serverconn()
    #             cur = conn1.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn1.commit()
    #             conn2 = localconn()
    #             cur = conn2.cursor()
    #             cur.execute(sqli, tuple(param))
    #             conn2.commit()
    #     except Exception as e:
    #         print(param[0],e)
    #         Errorlist.append((param[0], e))
    # # f.close()
    return Errorlist
if __name__ == '__main__' :
    gbk_to_utf8()
    # concept_errorlist = update_dzhconcept(ser='both') # 注意导出数据是否完整 文件编码
    # dfErrorList = pd.DataFrame( concept_errorlist)
    # dfErrorList.to_csv(path() + '/error/dzhconcept.csv')
    # print(dfErrorList)
    # control_errorlist = update_dzhcontrol(ser='both') # 注意导出数据是否完整 文件编码
    # dfErrorList2 = pd.DataFrame( control_errorlist)
    # dfErrorList2.to_csv(path() + '/error/dzhcontrol.csv')
    # print(dfErrorList2)
    capitalchange_errorlist = update_capitalchange(ser='both') # 改抬头，删字段，数字格式
    dfErrorList3 = pd.DataFrame(capitalchange_errorlist)
    dfErrorList3.to_csv(path() + '/error/capitalchange.csv')
    print(dfErrorList3)
    # buyback_errorlist = update_buyback(ser='both') # 改抬头，删字段，数字格式，文件编码
    # dfErrorList4 = pd.DataFrame(buyback_errorlist)
    # dfErrorList4.to_csv(path() + '/error/update_buyback.csv')
    # print(dfErrorList4)
    # incentive_errorlist = update_incentive(ser='both') # 改抬头，删字段，数字格式，文件编码
    # dfErrorList5 = pd.DataFrame(incentive_errorlist)
    # dfErrorList5.to_csv(path() + '/error/update_incentive.csv')
    # print(dfErrorList5)