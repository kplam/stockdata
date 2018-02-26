import pandas as pd
from kpfunc.function import *
from kpfunc.getdata import *
from kpfunc.spyder import *
from numpy import nan
import tushare,numpy
from bs4 import BeautifulSoup as bs
conn=localconn()
df = pd.read_csv('./data/dzhdata/delisted.csv',encoding='gbk',dtype='object')

df['交易状态']='-1'
df['拼音缩写']=[getpinyin(df['证券简称'][i]) for i in range(len(df))]

codes = df['证券代码'].values
# for code in codes:
#     code_pre = "SH" + code if code[0] == '6' else "SZ" + code
#
#     try:
#         delist=pd.read_csv('E:/TXTDAY/'+code_pre+".csv",names=['date','open','high','low','close','vol','amo'])
#         delist['code']=code
#         delist.to_sql('dayline',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
#     except:
#         print(code_pre)
# print(df)
# df_stocklist = df[['证券代码','证券简称','上市市场','交易状态','拼音缩写']]
# print(df_stocklist)
# df_stocklist.to_sql('stocklist',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
# df_basedata = df[['公司名称','英文名称','成立日期','工商登记号','注册资本','法人代表','所属证监会行业','员工总数','所属地区','所属城市','注册地址','办公地址','邮编','电话','传真','电子邮箱','公司网站','总经理','董事会秘书','审计机构','首发日期','首发价格','证券代码']]
# df_basedata = df_basedata.replace(nan,'')
# sql="update `basedata` set `公司名称`=%s,`英文名称`=%s,`成立日期`=%s,`工商登记号`=%s,`注册资本`=%s,`法人代表`=%s,`所属证监会行业`=%s,`员工总数`=%s,`省份`=%s,`城市`=%s,`注册地址`=%s,`办公地址`=%s,`邮编`=%s,`电话`=%s,`传真`=%s,`电子邮件`=%s,`公司网站`=%s,`总经理`=%s,`董事会秘书`=%s,`审计机构`=%s,`首发日期`=%s,`首发价格`=%s WHERE `证券代码`=%s"
# for elem in df_basedata.values:
#     # param = (str(pa) for pa in elem)
#     try:
#         cur=conn.cursor()
#         cur.execute(sql,tuple(elem))
#         conn.commit()
#     except:
#         print(elem[-1])
# df = tushare.get_k_data('sz000003')
# print(df)
# name='PT金田A'
# print(hex(name))
for code in codes:
    url = "http://stock.finance.qq.com/corp1/distri.php?zqdm=%s"%(code)
    # print(pd.read_html(url))
    html=myspyder(url,proxy=0).content.decode('gbk')
    Soup=bs(html,'html5lib')
    list=Soup.find_all('table')
    fhsz = []
    pg = []
    for i in range(len(list)):
        if i < len(list)-1:
            tds =list[i].select('.fntTahoma')
            fhsz =fhsz+[td.text for td in tds]
        else:
            tds = list[i].select('.fntTahoma')
            pg = [td.text for td in tds]
    # print(fhsz)
    print(code,pg)
    # fhsz = numpy.array(fhsz).reshape(int(len(fhsz)/7),7)
    # df_fhsz = pd.DataFrame(fhsz,columns=['年度','每股收益','送股','转增',	'红利','登记日','date'])
    # df_fhsz['code']=code
    # df_fhsz=df_fhsz[['code','date','送股','转增','红利']]
    # df_fhsz=df_fhsz.replace('--',0)
    # df_fhsz=df_fhsz[df_fhsz['date']!=0]
    # df_fhsz['送股'] = df_fhsz['送股'].astype(float)
    # df_fhsz['转增'] = df_fhsz['转增'].astype(float)
    #
    # df_fhsz['红股'] = df_fhsz['送股']+df_fhsz['转增']
    # df_fhsz=df_fhsz[['code','date','红股','红利']]
    # # df_fhsz.to_sql('ftsplit',conn,flavor='mysql',schema='stockdata',if_exists='append',index=False)
    # for param in df_fhsz.values:
    #     sql ="insert ignore into `ftsplit` (`code`,`date`,`红股`,`红利`) value(%s,%s,%s,%s) "
    #     cur=conn.cursor()
    #     cur.execute(sql,tuple(param))
    #     conn.commit()
    # print(df_fhsz)