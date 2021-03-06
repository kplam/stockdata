from kpfunc.getdata import get_stocklist_prefix
from kpfunc.spyder import myspyder
from kpfunc.function import GetFileList
import json,re,datetime,gzip,zipfile,os
import pandas as pd
import gevent
from gevent import monkey
from gevent.pool import Pool

def get_tick_detail(code):
    # print(code[:-1])
    url = "http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&id=%s&page=1&rows=10000&gtvolume=&sort=desc"%(code)
    html ="error!"
    times_retry = 10
    while (html == "error!" or html.status_code!=200)  and times_retry != 0:
        html = myspyder(url,proxy=0)
        times_retry -= 1
    if html.status_code==200:
        try:
            html = json.loads(html.content.decode('utf-8')[1:-1])
            table=[]
            for i in html['value']['data']:
                    table.append(re.split(",",i))
            df =pd.DataFrame(table,columns=['time','price','vol',1,2,3,4,'成交笔数'])
            with open("./data/tick/"+code[:-1]+"_"+str(datetime.date.today())+".jz",'wb') as f:
                jz = json.dumps(html['value']['data']).encode('utf-8')
                jz = gzip.compress(jz,compresslevel=9)
                f.write(jz)
        except:
            pass


def update_tick(poolnum=500):
    print("TICK:正在更新成交明细...")
    monkey.patch_all()
    gpool = Pool(poolnum)
    stocklist=get_stocklist_prefix('1','2',0)
    tasks = [gpool.spawn(get_tick_detail,code) for code in stocklist]
    gevent.joinall(tasks)
    print("TICK:更新完成！")

def zipfiles(N=0):
    filelist = GetFileList("./data/tick/")
    today = str(datetime.date.today()-datetime.timedelta(days=N))
    zipf = zipfile.ZipFile("./data/tick/zip/"+today+".zip", 'w')
    # for parent, dirnames, filenames in os.walk("./data/tick/2018-03-01/"):

    for filename in filelist:
        if today in filename:
            # pathfile = os.path.join(filename)
            # arcname = pathfile[12:].strip(os.path.sep)  # 相对路径
            zipf.write(filename, compress_type=zipfile.ZIP_LZMA)
            os.remove(filename)
    zipf.close()


if __name__ == '__main__':
    t=datetime.datetime.today()
    update_tick(poolnum=500)
    t=datetime.datetime.today()-t
    print(t)
    zipfiles()
