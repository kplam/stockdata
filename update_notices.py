#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-06

@author: kplam
"""

from kpfunc.spyder import myspyder
from kpfunc.getdata import *
from kpfunc.function import path
from time import sleep
from random import random
import datetime,json
import pandas as pd



def notices(page,ser='both',proxy=0):
    today=datetime.date.today() #- datetime.timedelta(days=2)
    sleep(random()/10*2+0.5)
    print("NOTICE：page",page)
    engine=conn()
    try:

        url = "http://data.eastmoney.com/notices/getdata.ashx?FirstNodeType=0&CodeType=1&PageIndex=%s&PageSize=1000"%(page)
        html = myspyder(url,proxy=proxy).content
        js =json.loads(html.decode('gbk')[7:-1])['data']

        table=pd.DataFrame()
        for i in range(len(js)):
            output =js[i]
            output1 =js[i]['CDSY_SECUCODES'][0]
            output2 =js[i]['ANN_RELCOLUMNS'][0]
            output3 =js[i]['ANN_RELCODES'][0]
            del output['CDSY_SECUCODES'] ,output['ANN_RELCOLUMNS'], output['ANN_RELCODES']
            output.update(output1)
            output.update(output2)
            output.update(output3)
            output['NOTICEDATE'] = output['NOTICEDATE'][:-6]
            output['EUTIME'] = output['EUTIME'][:-6]
            output['Url'] = "http://pdf.dfcfw.com/pdf/H2_"+output['INFOCODE']+"_1.pdf" if output['ATTACHTYPE']=='0' else output['Url']
            tmp_table =pd.DataFrame.from_dict(output,orient='index')
            table =pd.concat((tmp_table.T,table),ignore_index=True)
        table=table[['NOTICEDATE','NOTICETITLE','INFOCODE','EUTIME','Url','SECURITYCODE','SECURITYFULLNAME','SECURITYTYPE','TRADEMARKET','COLUMNNAME']]
        table['NOTICEDATE']=table['NOTICEDATE'].astype('datetime64[ns]')
        table['EUTIME']=table['EUTIME'].astype('datetime64[ns]')
        table = table.rename(columns={'NOTICEDATE':'date','NOTICETITLE':'title','INFOCODE':'infocode','EUTIME':'eutime',
                                      'Url':'url','SECURITYCODE':'code','SECURITYFULLNAME':'name','SECURITYTYPE':'security_type',
                                      'TRADEMARKET':'market','COLUMNNAME':'type'})
        table=table[table['eutime']>=today]
        # table.to_csv(path()+'/data/notice/'+str(today)+'.csv',encoding='utf-8')


        sql_check="select `infocode` from `notice` where `eutime`>'%s'"%(today-datetime.timedelta(days=1))

        list_infocode=pd.read_sql(sql_check,engine)['infocode'].values


        for line in table.values:
            param = [str(ele) for ele in line]
            if param[2] not in list_infocode:
                sql_updae =" insert ignore into `notice` (`date`, `title`, `infocode`, `eutime`, `url`, `code`, `name`, " \
                           "`security_type`, `market`, `type`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                engine.execute(sql_updae,tuple(param))
                # conn.commit()

            else:
                pass
        # return None
    except Exception as e:
        print(e)
        return page

if __name__ =="__main__":
    pages = range(1,2)[::-1]
    times_retry = 3
    while len(pages) != 0 and times_retry != 0 :
        pages = [notices(page,ser='local') for page in pages]
        pages = list(set(pages))
        try:
            pages.remove(None)
        except:
            pass
        times_retry -= 1
