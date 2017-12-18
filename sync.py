import pandas as pd
from kpfunc.getdata import *
import datetime
from numpy import NaN
from math import isnan


local = localconn()
server = serverconn()
today =datetime.date.today() # -datetime.timedelta(days=3)
# print(today)
# sql_getdate = "SELECT DISTINCT `date` FROM `usefuldata` ORDER BY `date` DESC limit 1"
# dates=pd.read_sql(sql_getdate,serverconn()).values
def sync(sdate):
    try:
        sql_del = "delete from `usefuldata` WHERE `date`='%s'"%(sdate)
        # sql_dayline = "Select * from `dayline` WHERE `date`>='2017-11-10'"
        sql_usefuldata = "Select * from `usefuldata` WHERE `date`='%s'"%(sdate)
        # dayline = pd.read_sql(sql_dayline,server)
        cur=local.cursor()
        cur.execute(sql_del)
        local.commit()
        usefuldata = pd.read_sql(sql_usefuldata,serverconn())
        # dayline.to_sql('dayline',local,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
        usefuldata.to_sql('usefuldata',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=1000)
    except Exception as e:
        print(e)


# for sdate in dates:
#     print(str(sdate[0]))
#     sync(str(sdate[0]))
if __name__ == '__main__':
    sync(str(today))
