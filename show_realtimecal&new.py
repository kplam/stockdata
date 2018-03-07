from kpfunc.getdata import *
import time,datetime


today = datetime.date.today()
wd = datetime.date.today().weekday()
wdlist='一二三四五六日'
print("今天是%s, 星期%s。 "%(today,wdlist[wd]))
engine=conn()
sql_news_id = "select `id` from `news` WHERE datetime<'%s' ORDER BY `id` DESC limit 1" % (str(today))
sql_realtime_id = "select `id` from `realtimecal`  WHERE datetime<'%s' ORDER BY `id` DESC limit 1"%(str(today))
id = pd.read_sql(sql_news_id,engine)['id'][0]
id2 = pd.read_sql(sql_realtime_id,engine)['id'][0]
sleeptime = 300

while True:
    try:
        sql_news ="select `id`, `datetime`, `type` ,`title` from `news` where id > %s ORDER BY `id` ASC "%(id)
        result = engine.execute(sql_news).fetchall()
        for row in result:
            print(str(row[1])[11:16],(row[2]+row[3])[:34])
            id = row[0]

        if sleeptime%300==0:
            sql_realtime = "select `id`,`datetime`,`taresult`,`finalresult` from `realtimecal` where id>%s ORDER BY `id` ASC " % (id2)

            results = engine.execute(sql_realtime).fetchall()
            if len(results)>0:
                row=results[-1]
                # for row in results:
                print("\n"+"=" * 80)
                print("+"*34 +"实时选股结果"+"+"*34)
                print("=" * 80)
                print("当前运算时间:%s"%str(row[1]))
                print("+"*80)
                print("技术分析结果:\n")
                print(row[2])
                print("+"*80)
                print("综合结果:\n")
                print(row[3] if row[3] else "空")
                print("="*80+"\n")
                id2 = row[0]
    except Exception as e:
        print(e)
    finally:
        time.sleep(30)
        sleeptime+=30
