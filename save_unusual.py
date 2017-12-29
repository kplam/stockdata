#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 15:20:00 2017-12-09

@author: kplam
"""

"""
http://nuyd.eastmoney.com/EM_UBG_PositionChangesInterface/api/js?style=top&js=[(x)]&ac=normal&dtformat=HH:mm:ss
"""
from kpfunc.spyder import myspyder
from kpfunc.function import path,GetFileList
from kpfunc.getdata import localconn,serverconn
import datetime,json,re,gzip,time
import pandas as pd
# import gevent
# from gevent import monkey; monkey.patch_all()
# from gevent.pool import Pool
# from pytagcloud import create_tag_image, make_tags
# # from pytagcloud.lang.counter import get_tag_counts

from collections import Counter

def unusual():
    url = "http://nuyd.eastmoney.com/EM_UBG_PositionChangesInterface/api/js?style=top&js=[(x)]&dtformat=HH:mm:ss&ac=normal"
    html = myspyder(url,0).content.decode('utf-8')
    return html
def analysis(ser='both'):
    # print("UNUSUAL: Running...")
    today = datetime.date.today()
    now=datetime.datetime.today() - datetime.timedelta(minutes=5)
    data = json.loads(unusual())
    table = [re.split(",",ele) for ele in data]
    for elem in table:
        elem[0]= elem[0][:-1]
    df = pd.DataFrame(table,columns=['code','name','time','tcode','type','data','goodorbad'])
    js = df.to_json(orient='records', force_ascii=False).encode('utf-8')
    if int(time.strftime("%H%M%S"))>150000:
        with open(path() + "/data/unusual/" + str(today) + ".jz", 'wb') as f:
            f.write(gzip.compress(js, compresslevel=9))
    df['date']=str(today)
    df['datetime']=df['date']+" "+df['time']
    df['datetime']=pd.to_datetime(df['datetime'])
    df = df[['datetime','code','type','data','goodorbad']]
    df = df[df['datetime']>=now]

    if ser == 'local' or ser == 'both':
        conn = localconn()
    if ser == 'server' or ser == 'both':
        conns = serverconn()

    for param in df.values:

        sql_update = "insert ignore into `unusual`(`datetime`, `code`, `type`, `data`, `goodorbad`) value(%s,%s,%s,%s,%s)"
        param = (str(param[0]),param[1],param[2],param[3],param[4])
        if ser == 'local' or ser == 'both':
            cur=conn.cursor()
            cur.execute(sql_update,tuple(param))
            conn.commit()
        if ser == 'server' or ser == 'both':
            curs=conns.cursor()
            curs.execute(sql_update,tuple(param))
            conns.commit()
    # print("UNUSUAL: Done!")
    # df.to_sql('unusual',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False)
    # counts = Counter(df['code'].values).items()
    # print(pd.DataFrame(list(counts),columns=['code','times']).to_json(orient='records',force_ascii= False))
    return df
if __name__ == '__main__':
    # monkey.patch_all()
    df = analysis(ser='both')
    # filelist= GetFileList(path()+"/data/unusual/")
    # for file in filelist:
    #     print(file[-13:-3])
    #     with open(file,'rb')as f:
    #         jz = f.read()
    #         js = gzip.decompress(jz)
    #         df =pd.read_json(js,dtype='object')
    #         df['date'] = str(file[-13:-3])
    #         df['datetime'] = df['date'] + " " + df['time']
    #         # df['datetime'] = pd.to_datetime(df['datetime'])
    #
    #         df = df[['datetime', 'code', 'type', 'data', 'goodorbad']]
    #         print(df)
    #         # df = df[df['datetime'] >= now]
    #         df['datetime'] = df['datetime'].astype('object')
    #         try:
    #             df.to_sql('unusual',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False)
    #         except:
    #             pass
    # class stocktag:
    #     def __init__(self):
    #         self.list=[]
    #
    #     def get_basedata(self,ele):
    #         sql="select `所属主题`,`所属概念` from `basedata` WHERE `证券代码`=%s"%(ele[0])
    #         df_tmp=pd.read_sql(sql,localconn())
    #         df_tmp=df_tmp.fillna('')
    #         data = df_tmp.values[0]
    #         subject=[]
    #         try:
    #             subject = data[0]
    #             subject= re.split(",",subject)
    #         except:
    #             pass
    #         concept=[]
    #         try:
    #             concept = data[1]
    #             concept = re.split(",",concept)
    #         except:
    #             pass
    #         self.list =self.list + [ele[1]]#, ele[4]] #+ subject + concept
    #         return None
    # tPool=Pool(100)
    # st=stocktag()
    # tasks = [tPool.spawn(st.get_basedata,ele) for ele in df.values]
    # gevent.joinall(tasks)
    # print(st.list)
    # counts = Counter(st.list).items()
    # # print(counts)
    # tags = make_tags(counts, maxsize=50)
    # create_tag_image(tags, 'cloud_large.png', size = (1920, 300), fontname ='Yahei',rectangular=False)