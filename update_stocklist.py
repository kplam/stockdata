#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-01
@author: kplam
"""
from kpfunc.getdata import *
from kpfunc.spyder import myspyder
from kpfunc.function import getpinyin,path
import pandas as pd
import re,datetime

def update_stocklist(proxy=0):
    """

    :param proxy: 0 close / 1 open
    :return: errorlist
    """
    url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=NS&sty=NSSTV5&st=12&sr=true&p=1&ps=100"
    html = "error!"
    times_retry = 3
    while html == "error!" and times_retry != 0:
        html = myspyder(url=url, proxy=proxy)
        times_retry -= 1

    try:
        html_doc = str(html.content, 'utf-8')
        return_list = re.findall("\"(.*?)\"", html_doc)
        xgtable = [re.split("\,", elem) for elem in return_list]
        # xg = [[xglist[3],xglist[4],xglist[10],xglist[13]] for xglist in xgtable ]
        xg = pd.DataFrame(xgtable)
        xg = xg[[3, 4, 10, 13]].rename(columns={3:"name",4:"code",10:"ipoprice",13:"ipodate"})
        xg['ipodate'] = xg['ipodate'].astype('datetime64[ns]')
        xg['name'] = xg['name'].astype('str')
        xg['code'] = xg ['code'].astype('str')
        xg = xg.dropna().reset_index(drop=True)
        print("STOCKLIST:数据获取成功，正在写入数据库...")

        engine=conn()

        stocklist = get_stocklist()
        Errorlist =[]
        sql_ipocheck = "select `证券代码` from `basedata` WHERE `首发价格` is NULL"
        ipocheck = pd.read_sql(sql_ipocheck,engine)['证券代码'].values


        for i in range(len(xg)):
            code, name = xg['code'][i], xg['name'][i]
            ipoprice , ipodate = xg['ipoprice'][i], xg['ipodate'][i]
            pinyin = getpinyin(name) if '银行' not in name else getpinyin(name).replace('YX','YH')
            market = '上海证券交易所' if code[0] == '6' else '深圳证券交易所'
            if code not in stocklist or code in ipocheck:
                try:
                    sql_xg = "INSERT ignore INTO `stocklist`(`证券代码`, `证券简称`, `上市市场`,`拼音缩写`) VALUES (%s,%s,%s,%s)"
                    sql_ipo = "update `basedata` set `首发日期`=%s ,`首发价格`=%s WHERE `证券代码`=%s"

                    engine.execute(sql_xg, (code, name, market, pinyin))
                    # conn.commit()
                    engine.execute(sql_ipo, (str(ipodate), ipoprice, code))
                    # conn.commit()

                    print("STOCKLIST:",code, "：更新成功！")
                except Exception as e:
                    print("STOCKLIST:",code, "：更新失败！", e)
                    Errorlist.append(code)

        output = str(datetime.date.today())+ (" 更新完成！" if len(Errorlist) == 0 else " 更新出错！请检查！")
        print("STOCKLIST:",output)
        return Errorlist
    except:
        return ['数据获取失败...']

if __name__ == "__main__" :
    error = update_stocklist(proxy=0)
    df_error = pd.DataFrame(error)
    df_error.to_csv(path()+'/error/update_stocklist.csv')