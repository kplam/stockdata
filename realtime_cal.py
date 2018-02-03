from kpfunc.getdata import *
from kpfunc.spyder import myspyder
from kpfunc.indicator import *
from update_dayline import *
from cal_financial import *
import time, math, os

class realtime_cal:
    def __init__(self):
        self.dfrealtime = pd.DataFrame()
        self.stocklist = get_stocklist()
        self.lastamorank = pd.DataFrame()
        self.jma_result = []
        self.macd_result = []
        self.findate = '2017-09-30'
        self.forecastdate = '2017-12-31'
        self.today = datetime.date.today()
        self.list_fr = []
        self.list_fm = []
        self.list_forecast = []
        self.list_spo= []
        self.baselist = []

    def fr(self):
        sql_fr = "select * from `financial_rank` WHERE `总评分`>63 and `报表日期`='%s'" % (self.findate)
        self.list_fr = pd.read_sql(sql_fr, localconn())['代码'].values
        return self.list_fr

    def fmedian(self):
        self.list_fm = cal_financial(localconn()).median()
        return self.list_fm

    def forecast(self):
        sql_forecast = "select * from `forecast` WHERE `同期净利润`>10000000 and `上限`>30 and `财报日期`='%s'" %(self.forecastdate)
        self.list_forecast = pd.read_sql(sql_forecast,localconn())['code'].values
        return self.list_forecast

    def spo(self):
        sql_spo = "select `code` from `spo_done` WHERE `发行日期`>'%s'" %(self.today-datetime.timedelta(days=365*2))
        self.list_spo = list(set(pd.read_sql(sql_spo,localconn())['code'].values))
        return self.list_spo

    def getbase(self):
        print("正在计算基本面股票池...")
        alllist = [self.fr(), self.fmedian(), self.forecast(), self.spo()]
        for i, stocks in enumerate(alllist):
            if i == 0:
                self.baselist = stocks
            else:
                self.baselist = list(set(self.baselist).intersection(stocks))
        return self.baselist


    def amorank(self):
        self.dfrealtime = update_bar().todf_stock()
        self.dfrealtime = self.dfrealtime.sort_values('amo',ascending=False).reset_index(drop=True)
        self.dfrealtime['amorank'] = pd.Series(np.arange(len(self.dfrealtime['date'])) + 1, index=self.dfrealtime.index)

    def last_amorank(self):
        lastamorank_result =[]
        for code in self.stocklist:
            sql = "select `amorank` from `usefuldata` where `code`='%s' order by `date` Desc limit 1"%(code)
            df = pd.read_sql(sql,localconn())['amorank']
            if df.empty ==False:
                lastamorank_result.append([code,df.values[0]])
        self.lastamorank = pd.DataFrame(lastamorank_result,columns=['code','lastamorank'])

    def cal_araise(self):
        self.dfrealtime = pd.merge(self.dfrealtime,self.lastamorank)
        self.dfrealtime['araise'] =self.dfrealtime['amorank']-self.dfrealtime['lastamorank']
        list_araisecompare = []
        for i in range(len(self.dfrealtime)):
            lastamorank = self.dfrealtime['lastamorank'][i]
            araisecompare = -1 / max(math.log((lastamorank), math.e), 1) * 1.25 * (lastamorank)
            list_araisecompare.append(araisecompare)
        self.dfrealtime['araisecompare'] = list_araisecompare

    def calc(self):
        lenstocklist=len(self.stocklist)
        df =self.dfrealtime[(self.dfrealtime['amorank']<=(lenstocklist//6)) & (self.dfrealtime['araise']<self.dfrealtime['araisecompare'])]
        df = df.reset_index(drop=True)
        self.jma_result = []
        self.macd_result = []
        for i in range(len(df)):
            code = df['code'][i]
            date = df['date'][i]
            preclose = df['preclose'][i]
            close = df['close'][i]
            open = df['open'][i]
            high = df['high'][i]
            low = df['low'][i]
            amo = df['amo'][i]
            vol = df['vol'][i]

            sql = "select * from `dayline` WHERE `code`='%s' ORDER BY `date` DESC limit 300"%(code)
            k = pd.read_sql(sql,localconn())
            maxadjcump = k.get_value(len(k) - 1, 'adjcump')
            k['date'] = k['date'].astype('datetime64[ns]')

            if abs(k['close'][0] - preclose) <0.0001:
                adjfactor = k['adjfactor'][0]
                adjcump = k['adjcump'][0]
                realtimelist = [[code, date, high, open, low, close, vol, amo, adjfactor, adjcump]]
                dftmp = pd.DataFrame(realtimelist,columns=['code', 'date', 'high', 'open', 'low', 'close', 'vol', 'amo', 'adjfactor',
                                              'adjcump'])
                dftmp['date']=dftmp['date'].astype('datetime64[ns]')
                k = pd.concat((k,dftmp))
                k = k.sort_values('date',ascending=True).reset_index(drop=True)
            else:
                adjfactor = preclose/k['close'][0]
                adjcump = adjfactor*k['adjcump'][0]
                maxadjcump = adjcump
                realtimelist = [[code, date, high, open, low, close, vol, amo, adjfactor, adjcump]]
                dftmp = pd.DataFrame(realtimelist,
                                     columns=['code', 'date', 'high', 'open', 'low', 'close', 'vol', 'amo', 'adjfactor',
                                              'adjcump'])
                dftmp['date'] = dftmp['date'].astype('datetime64[ns]')
                k = pd.concat((k, dftmp))
                k = k.sort_values('date', ascending=True).reset_index(drop=True)

            if len(k)>88:
                # ============== prepare data to calculate ==============#
                dayline_high = (k['high']/(maxadjcump/k['adjcump'])).values
                dayline_open = (k['open']/(maxadjcump/k['adjcump'])).values
                dayline_low = (k['low']/(maxadjcump/k['adjcump'])).values
                dayline_close = (k['close']/(maxadjcump/k['adjcump'])).values
                dayline_vol = k['vol'].values
                dayline_amo = k['amo'].values

                # ===============indicator calculate======================#
                k['jll'], k['jlh'] = jl(dayline_open, dayline_close, dayline_high, dayline_low, dayline_amo)
                k['js'] = js(dayline_open, dayline_close, dayline_high, dayline_low, dayline_amo)
                k['kprsi'] = kprsi(dayline_close)
                k['diff'], k['dea'], k['hist'] = macd(dayline_close)
                k = k[len(k) - 2:]
                k = k.reset_index(drop=True)

                for j in range(len(k)):
                    if j > 0 and isnan(k.get_value(j, 'jlh')) != True:
                        close_cp = k.get_value(j, 'close')
                        close_cp_ref = k.get_value(j - 1, 'close')
                        jshort_cp = k.get_value(j, 'js')
                        jlh_cp = k.get_value(j, 'jlh')
                        kprsi_cp = k.get_value(j, 'kprsi')
                        if close_cp_ref < jshort_cp and close_cp > jshort_cp and close_cp > jlh_cp and close_cp > kprsi_cp:
                            self.jma_result.append(code)
                    if j>0 and isnan(k.get_value(j,'hist')) != True:
                        diff = k.get_value(j,'diff')
                        dea = k.get_value(j,'dea')
                        diffref = k.get_value(j-1,'diff')
                        dearef = k.get_value(j-1,'dea')
                        if diff > 0 and diff >dea and diffref<dearef:
                            self.macd_result.append(code)
        return self.macd_result, self.jma_result

if __name__ == '__main__':
    tt0 = datetime.datetime.today()
    print("=" * 60)
    print("正在初始化...")
    rc=realtime_cal()
    rc.getbase()
    rc.last_amorank()
    base = rc.baselist
    tt1 = datetime.datetime.today()
    print("初始化完成,耗时%s"%(str(tt1-tt0)))
    print("=" * 60)
    print("交易时间内每隔5分钟计算一次...\n临近收盘计算结果更为可靠.")
    print("=" * 60)
    i = 1
    while 93000< int(time.strftime("%H%M%S"))<150001:
        if int(time.strftime("%H%M%S"))<113000 or int(time.strftime("%H%M%S"))>130000:
            tt00 =datetime.datetime.today()
            print("当前时间为：%s"%(tt00))
            print("正在进行第%i次计算"%(i))
            t1=int(time.strftime("%H%M%S"))
            rc.amorank()
            rc.cal_araise()
            macdresult, jmaresult = rc.calc()
            taresult=list(set(jmaresult+macdresult))
            finalresult = list(set(taresult).intersection(base))
            tt44 = datetime.datetime.today()
            print("计算完毕,耗时%s"%(str(tt44-tt00)))
            print("=" * 60)
            print("技术分析结果:\n", str(taresult)[1:-1])
            print("=" * 60)
            print("综合结果：\n", str(finalresult)[1:-1])
            print("=" * 60)
            t2 = int(time.strftime("%H%M%S"))
            i += 1
            time.sleep(60-(t2-t1))
        else:
            time.sleep(1)
    print("股市收盘，任意键退出。")
    os.system('pause')