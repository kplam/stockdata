# -*- coding: utf-8 -*-
#!/usr/bin/env/ python3
"""
Created on Thu May  4 15:20:00 2017

@author: kplam
"""


from package.function import *
import pandas as pd
import pymysql


# ========global variable========= #

errorList = []

# ===========sql connect========== #
conn = pymysql.connect(host='192.168.1.111', port=3306, user='root', passwd='1',
                       db='stockdata', charset='utf8')
cur = conn.cursor()
# ==========get filelist========= #
FileList = GetFileList(path()+"/5min/")

# ===========to sql============= #
for iIndex, file in enumerate(FileList):
    try:
        df = pd.read_csv(FileList[iIndex],encoding='gb2312',names=['date','min','open','high','low','close','vol','amo'])
        df['code']=FileList[iIndex][-10:-4]
        df=df[0:-1]
        print(FileList[iIndex][-10:-4])
        df.to_sql('5min', con=conn, flavor='mysql', if_exists='append',index=False, index_label='date', dtype=None)
    except Exception as e:
        print(e)
        errorList.append([file, e])

print("Done!")
dfErrorList = pd.DataFrame({'error': errorList})
dfErrorList.to_csv(path+'/error/history_5min.csv')
print(dfErrorList)