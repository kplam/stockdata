import pandas as pd
from kpfunc.getdata import *
import datetime
from numpy import NaN
from math import isnan


local = localconn()
server = serverconn()
# today = datetime.date.today() #-datetime.timedelta(days=1)
today = datetime.date(2018,1,5)

def sync(sdate):
    try:
        sql_usefuldata = "Select * from `usefuldata` WHERE `date`='%s' and `focus`!='' and `amorank` is null"%(sdate)
        usefuldata = pd.read_sql(sql_usefuldata,serverconn())
        usefuldata.to_sql('usefuldata',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=1000)
        sql_usefuldata_update = "Select * from `usefuldata` WHERE `date`='%s' and `focus`!='' and `amorank` is not null"%(sdate)
        usefuldata_update = pd.read_sql(sql_usefuldata_update,serverconn())
        for i in range(len(usefuldata_update)):
            code = usefuldata_update['code'][i]
            date = str(usefuldata_update['date'][i])
            focus = usefuldata_update['focus'][i]
            sql_update = "update `usefuldata` set `focus`=%s WHERE `code`=%s and `date`=%s"
            cur = local.cursor()
            cur.execute(sql_update,(focus,code,date))
            local.commit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    sync(str(today))
