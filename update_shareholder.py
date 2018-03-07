#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-11-22

@author: kplam
"""
from kpfunc.getdata import *
from kpfunc.spyder import myspyder
import warnings,json
import pandas as pd


"""
http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=sh600313
"""

def get_shareholder_data(stocklist =get_stocklist_prefix('sh','sz',1)):
    errorlist = []
    engine=  conn()
    for code in stocklist:


        url = "http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code=%s"%(code)
        html = myspyder(url,proxy=0)

        try:
            doc = json.loads(html.content)
            ##  get shareholder data
            if len(doc['sdgd'])>0:
                for i in range(len(doc['sdgd'])):
                    table = pd.DataFrame(doc['sdgd'][i]['sdgd'])
                    del table['bdbl']
                    table =table.rename(columns={'cgs':'quantity', 'gdmc':'name','gflx':'type','mc':'rank','rq':'date','zj':'change','zltgbcgbl':'percentage'})
                    table['code'] = code[2:]
                    table=table[['code','date','rank','name','quantity','percentage','change','type']]
                    for i in range(len(table)):
                        if table['change'][i]=='不变':
                            table['change'][i]=0
                        if table['change'][i]=='新进':
                            table['change'][i]=table['quantity'][i]

                        params=[str(param) for param in table.values[i]]
                        sql_query ="INSERT IGNORE INTO `shareholder`(`code`, `date`, `rank`, `name`, `quantity`, `percentage`, `change`, `type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        engine.execute(sql_query,params)

            ##  get cirholder data
            if len(doc['sdltgd'])>0:
                for j in range(len(doc['sdltgd'])):
                    table2 = pd.DataFrame(doc['sdltgd'][j]['sdltgd'])
                    del table2['bdbl']
                    table2 =table2.rename(columns={'cgs':'quantity', 'gdmc':'name','gdxz':'type','gflx':'abh','mc':'rank','rq':'date','zj':'change','zltgbcgbl':'percentage'})
                    table2['code'] = code[2:]
                    table2=table2[['code','date','rank','name','type','quantity','percentage','change','abh']]
                    for i in range(len(table2)):
                        if table2['change'][i] == '不变':
                            table2['change'][i] = 0
                        if table2['change'][i] == '新进':
                            table2['change'][i] = table2['quantity'][i]

                        params=[str(param) for param in table2.values[i]]
                        sql_query="INSERT ignore INTO `cirholder`(`code`, `date`, `rank`, `name`, `type`, `quantity`, `percentage`, `change`, `abh`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        engine.execute(sql_query,params)

            ##股东人数
            if len(doc['gdrs'])>0:
                table3 = pd.DataFrame(doc['gdrs'])
                table3 = table3.rename(columns={'cmjzd': 'scr', 'gdrs': 'shareholders', 'gdrs_jsqbh': 'shschange', 'qsdgdcghj':'top10', 'qsdltgdcghj':'cirtop10', 'gj':'close', 'rjcgje':'avgamount', 'rjltg':'avgcirquantity', 'rjltg_jsqbh':'avgcirchange', 'rq':'date'})
                table3['code'] = code[2:]
                table3 = table3[['code','date','close','scr','top10','cirtop10','shareholders','shschange','avgamount','avgcirquantity','avgcirchange']]
                for i in range(len(table3)):
                    if '万'in table3['shareholders'][i]:
                        table3['shareholders'][i]=float(table3['shareholders'][i].replace('万',''))*10000
                    if '万'in table3['avgamount'][i]:
                        table3['avgamount'][i]=float(table3['avgamount'][i].replace('万',''))*10000
                    if '万'in table3['avgcirquantity'][i]:
                        table3['avgcirquantity'][i]=float(table3['avgcirquantity'][i].replace('万',''))*10000
                    params=[str(param) if param!='--' else None for param in table3.values[i]]
                    sql_query="INSERT IGNORE INTO `shareholdernumber`(`code`, `date`, `close`, `scr`, `top10`, `cirtop10`, `shareholders`, `shschange`, `avgamount`, `avgcirquantity`, `avgcirchange`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    engine.execute(sql_query, params)


        except Exception as e:
            errorlist.append(code)
            print("%s:%s"%(code,e))
        #
        # if ser == "both" or ser == "local":
        #     conn.close()
        # if ser == "both" or ser == "server":
        #     conns.close()

    return errorlist


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    stocklist = get_shareholder_data(stocklist=get_stocklist_prefix('sh','sz',pre=1))
    times_retry = 10
    while len(stocklist) != 0 and times_retry != 0:
        stocklist = get_shareholder_data(stocklist=stocklist)
        times_retry -= 1
    print(stocklist)