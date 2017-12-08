from kpfunc.spyder import *
import multiprocessing


# pool=multiprocessing.Pool(processes=10)

path ='ipcheck.csv'
# list = get_ip_list_online()
# print(len(list))

iplist_output=ip_check(path)
ip_list = pd.DataFrame(iplist_output, columns=['ip'])
ip_list.to_csv('ip.csv',str='a')