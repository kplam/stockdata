import pandas as pd
from kpfunc.getdata import *
import hashlib,datetime,time,random


def make_checkcode(conn=conn(),N=100):
    list=[]
    for i in range(N):
        now = str(datetime.datetime.today())
        code = hashlib.md5(now.encode('utf-8')).hexdigest()[:12]
        time.sleep(random.random())
        user_check= hashlib.md5(code.encode('utf-8')).hexdigest()
        list.append([code,user_check])
    df = pd.DataFrame(list,columns=['code','user_check'])
    print(df)
    df.to_sql('user_invitation',conn,schema='stockdata',if_exists='append',index=False)


if __name__ == '__main__':
    make_checkcode(conn=conn(),N=2)
