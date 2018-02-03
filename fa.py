import pandas as pd
import numpy as np
from kpfunc.getdata import localconn


def financial_rank(date):
    sql="select * from `financial` WHERE `报表日期`='%s'"%(date)
    df = pd.read_sql(sql,localconn())
    df['p1'] =(df['每股资本公积金']+df['每股未分配利润'])/df['每股主营收入']
    df = df.sort_values(by=['p1'], ascending=False)
    df['p1rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['可持续评分'] = 10/len(df)*(len(df)+1-df['p1rank'])
    df = df.sort_values(by=['主营业务收入增长率'], ascending=False)
    df['主营业务收入增长率rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['主营业务收入增长率评分'] = 10/len(df)*(len(df)+1-df['主营业务收入增长率rank'])
    df = df.sort_values(by=['净利润增长率'], ascending=False)
    df['净利润增长率rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['净利润增长率评分'] = 10/len(df)*(len(df)+1-df['净利润增长率rank'])
    df['成长评分']=(df['净利润增长率评分']+df['主营业务收入增长率评分'])/2
    df = df.sort_values(by=['三年平均净资收益率'], ascending=False)
    df['三年平均净资收益率rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['稳定性评分'] = 10/len(df)*(len(df)+1-df['三年平均净资收益率rank'])
    df = df.sort_values(by=['销售净利率'], ascending=False)
    df['销售净利率rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['产品评分'] = 10/len(df)*(len(df)+1-df['销售净利率rank'])
    df = df.sort_values(by=['三项费用比重'], ascending=True)
    df['三项费用比重rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['经营评分'] = 10/len(df)*(len(df)+1-df['三项费用比重rank'])
    df = df.sort_values(by=['应收账款周转天数'], ascending=True)
    df['应收账款周转天数rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['收款评分'] = 10/len(df)*(len(df)+1-df['应收账款周转天数rank'])
    df = df.sort_values(by=['资产负债率'], ascending=True)
    df['资产负债率rank'] = pd.Series(np.arange(len(df['代码'])) + 1, index=df.index)
    df['资产评分'] = 10/len(df)*(len(df)+1-df['资产负债率rank'])
    df['总评分']=df['可持续评分']+df['成长评分']*4+df['稳定性评分']+df['产品评分']+df['经营评分']+df['收款评分']+df['资产评分']
    df=df[['代码','名称','报表日期','可持续评分','成长评分','稳定性评分','产品评分','经营评分','收款评分','资产评分','总评分']]
    # df.to_sql('financial_rank',localconn(),flavor='mysql',schema='stockdata',if_exists='append',index=False)
    return df

if __name__ == '__main__':
    sql="select distinct `报表日期` from `financial`"
    datelist=pd.read_sql(sql,localconn())['报表日期'].values
    for date in datelist:
        financial_rank(str(date))
    # sql="select * from `financial_rank`"
    # df = pd.read_sql(sql,localconn())
    # print(df['总评分'].mean())
    # print(df['总评分'].median())
    # print(df['总评分'].std())