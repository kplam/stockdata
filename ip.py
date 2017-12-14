from kpfunc.spyder import *

def checkip():
    path ='ipcheck.csv'
    iplist_output=ip_check(path)
    ip_list = pd.DataFrame(iplist_output, columns=['ip'])
    ip_list.to_csv('ip.csv',str='a')

if __name__ == '__main__':
    checkip()
