import pandas as pd
from kpfunc.getdata import *
import datetime

local = localconn()
server = serverconn()
today =datetime.date.today() # -datetime.timedelta(days=3)
print(today)
sql_del = "delete from `usefuldata` WHERE `date`>='%s'"%(today)
# sql_dayline = "Select * from `dayline` WHERE `date`>='2017-11-10'"
sql_usefuldata = "Select * from `usefuldata` WHERE `date`>='%s'"%(today)
# dayline = pd.read_sql(sql_dayline,server)
cur=local.cursor()
cur.execute(sql_del)
local.commit()
usefuldata = pd.read_sql(sql_usefuldata,server)
# dayline.to_sql('dayline',local,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=10000)
usefuldata.to_sql('usefuldata',local,flavor='mysql',schema='stockdata',if_exists='append',index=False,chunksize=1000)