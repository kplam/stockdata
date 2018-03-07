from kpfunc.getdata import *
import pandas as pd
from numpy import nan
# from gevent import monkey;monkey.patch_all()
# from gevent.pool import Pool
# import gevent

class lhb_calc:
    def __init__(self):
        self.sql = "select distinct `code`,`date` from `lhb`"
        self.alldata = pd.read_sql(self.sql,conn()).values
        self.unit = pd.read_sql("select distinct `营业部代码`,`营业部名称` from `lhb`",conn()).values
        self.list =[]
        self.days = 0
        self.all = pd.read_sql("SELECT * from `lhb` LEFT JOIN `lhbper` ON `lhb`.`code`=`lhbper`.`code` and `lhb`.`date`=`lhbper`.`date`",conn())

    def getlhbpercentage(self, code, date):
        sql = "select `*` from `dayline` WHERE `date` > '%s' and `code` ='%s' ORDER BY `date` ASC Limit %s"\
              % (str(date), code, self.days)
        df0 = pd.read_sql(sql, conn())
        if len(df0)>1:
            df0=df0.values
            if abs(df0[0][3]-df0[0][5])>0.001 or abs(df0[0][2]-df0[0][4])>0.001:
                # if len(df0)>1:
                percentage = ((df0[len(df0)-1][5]*df0[len(df0)-1][9])/(df0[0][3]*df0[0][9])-1)*100
            else:
                percentage = None
        else:
            percentage = None
        return [code, date, percentage]

    def get_all(self,stocklist):

        errorlist = []
        i=0
        for code,date in stocklist:
            if code[0] in ['0','3','6']:
                try:
                    singleresult = lhb_calc.getlhbpercentage(self,code=code, date=date)
                    self.list.append(singleresult)
                    print(singleresult[0],str(singleresult[1]),str(round(singleresult[0],2)),round(i / len(self.alldata) * 100))
                except Exception as e:
                    print(e)
                    errorlist.append([code,date])
                finally:
                    i += 1
            else:
                i += 1
        return errorlist

    def retryerror(self,N):
        self.days = N
        errorlist = self.alldata
        print(errorlist)
        times_retry = 5
        while len(errorlist)!=0 and times_retry !=0:
           errorlist= lhb_calc.get_all(self,stocklist=errorlist)

    def list_to_csv(self):
        try:
            filename = "lhbpercentage_" + str(self.days) + ".csv"
            with open(filename,'w') as f:
                f.writelines('code' + ',' + 'date' + ',' + 'percentage' + '\n')
                for code,date,percentage in self.list:
                    f.writelines(str(code) + ',' + str(date) + ',' + str(percentage) + '\n')
            return True
        except:
            return False

    def clean(self):
        self.list=[]

    def win(self):
        with open('win2.csv','w') as f:
            f.writelines('uintcode,uintname,times,sum,p3a,p5a,p20a,p60a,p3,p5,p20,p60\n')
            for uintcode in self.unit:
                data = self.all[self.all['营业部代码']==uintcode[0]]
                data = data[data['买卖方向']=='2']
                if data.empty==False:
                    # data = data.replace('None',nan)
                    data['p3'] = data['p3'].astype('float')
                    data['p5'] = data['p5'].astype('float')
                    data['p20'] = data['p20'].astype('float')
                    data['p60'] = data['p60'].astype('float')
                    f.writelines(str((uintcode[0],uintcode[1],len(data),data['买入金额'].sum(),data['p3'].mean(),data['p5'].mean(),data['p20'].mean(),data['p60'].mean(),len(data[data['p3']<0])/len(data),len(data[data['p5']<0])/len(data),len(data[data['p20']<0])/len(data),len(data[data['p60']<0])/len(data)))+'\n')

if __name__ == '__main__':
    L = lhb_calc()
    L.win()
    # L.retryerror(N=3)
    # L.list_to_csv()
    # L.clean()
    #
    # L.retryerror(N=5)
    # L.list_to_csv()
    # L.clean()
    #
    # L.retryerror(N=20)
    # L.list_to_csv()
    # L.clean()
    #
    # L.retryerror(N=60)
    # L.list_to_csv()
    # L.clean()