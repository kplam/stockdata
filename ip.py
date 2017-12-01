from kpfunc.spyder import *
path ='ipcheck.csv'
iplist_output=ip_check(path)
ip_list = pd.DataFrame(iplist_output, columns=['ip'])
ip_list.to_csv('ip.csv')