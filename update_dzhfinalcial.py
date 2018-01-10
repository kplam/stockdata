#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri DEC 1 15:20:00 2017
"
@author: kplam
"""
from kpfunc.getdata import localconn,serverconn
from kpfunc.function import path
import pandas as pd

def update_financial(filename,conn=localconn()):
    file_path = path()+"/data/dzhfinancial/"+filename+".csv"
    df_data = pd.read_csv(file_path,encoding='gbk',dtype='object')
    list_data=df_data.values
    errorlist = []

    for i in range(len(list_data)):
        sql = "INSERT IGNORE INTO `financial`(`名称`, `报表日期`, `代码`, `摊薄每股收益`, `净资产收益率`, `每股经营活动现金流量`, `每股净资产`, `每股资本公积金`, `每股未分配利润`, `每股主营收入`, `扣除非经常损益每股收益`, `货币资金`, `交易性金融资产`, `应收票据`, `应收账款`, `预付款项`, `应收利息`, `应收股利`, `其他应收款`, `应收关联公司款`, `存货`, `消耗性生物资产`, `一年内到期的非流动资产`, `其他流动资产`, `流动资产合计`, `可供出售金融资产`, `持有至到期投资`, `长期应收款`, `长期股权投资`, `投资性房地产`, `固定资产`, `在建工程`, `工程物资`, `固定资产清理`, `生产性生物资产`, `油气资产`, `无形资产`, `开发支出`, `商誉`, `长期待摊费用`, `递延所得税资产`, `其他非流动资产`, `非流动资产合计`, `资产总计`, `短期借款`, `交易性金融负债`, `应付票据`, `应付账款`, `预收账款`, `应付职工薪酬`, `应交税费`, `应付利息`, `应付股利`, `其他应付款`, `应付关联公司款`, `一年内到期的非流动负债`, `其他流动负债`, `流动负债合计`, `长期借款`, `应付债券`, `长期应付款`, `专项应付款`, `预计负债`, `递延所得税负债`, `其他非流动负债`, `非流动负债合计`, `负债合计`, `实收资本或股本`, `资本公积`, `库存股`, `盈余公积`, `未分配利润`, `外币报表折算差额`, `非正常经营项目收益调整`, `股东权益合计不含少数股东权益`, `少数股东权益`, `股东权益合计含少数股东权益`, `负债和股东权益合计`, `营业收入`, `营业成本`, `营业税金及附加`, `销售费用`, `管理费用`, `堪探费用`, `财务费用z`, `资产减值损失`, `公允价值变动净收益`, `投资收益`, `对联合营企业的投资收益`, `影响营业利润的其他科目`, `营业利润`, `补贴收入`, `营业外收入`, `营业外支出`, `非流动资产处置净损失`, `影响利润总额的其他科目`, `利润总额`, `所得税费用`, `影响净利润的其他科目`, `净利润含少数股东损益`, `净利润不含少数股东损益`, `少数股东损益`, `销售商品、提供劳务收到的现金`, `收到的税费返还`, `收到的其他与经营活动有关的现金`, `经营活动现金流入小计`, `购买商品、接受劳务支付的现金`, `支付给职工以及为职工支付的现金`, `支付的各项税费`, `支付的其他与经营活动有关的现金`, `经营活动现金流出小计`, `经营活动产生的现金流量净额`, `收回投资所收到的现金`, `取得投资收益所收到的现金`, `处置固定、无形和其他长期资产收回的现金净额`, `处置子公司及其他营业单位收到的现金净额`, `收到的其他与投资活动有关的现金`, `投资活动现金流入小计`, `购建固定资产、无形资产和其他长期资产支付的现金`, `投资所支付的现金`, `取得子公司及其他营业单位支付的现金净额`, `支付其他与投资活动有关的现金`, `投资活动现金流出小计`, `投资活动产生的现金流量净额`, `吸收投资所收到的现金`, `子公司吸收少数股东权益性投资收到的现金`, `取得借款收到的现金`, `收到其他与筹资活动有关的现金`, `筹资活动现金流入小计`, `偿还债务支付的现金`, `分配股利、利润或偿付利息支付的现金`, `子公司支给付少数股东的股利、利润`, `支付其他与筹资活动有关的现金`, `筹资活动现金流出小计`, `筹资活动产生的现金流量净额`, `汇率变动对现金的影响`, `其他原因对现金的影响`, `现金及现金等价物净增加额`, `期初现金及现金等价物余额`, `期末现金及现金等价物余额`, `净利润`, `加：资产减值准备`, `固定资产折旧、油气资产折耗、生产性生物资产折旧`, `无形资产摊销`, `长期待摊费用摊销`, `处置固定资产、无形资产和其他长期资产的损失`, `固定资产报废损失`, `公允价值变动损失`, `财务费用l`, `投资损失`, `递延所得税资产减少`, `递延所得税负债增加`, `存货的减少`, `经营性应收项目的减少`, `经营性应付项目的增加`, `其他`, `债务转为资本`, `一年内到期的可转换公司债券`, `融资租入固定资产`, `现金的期末余额`, `现金的期初余额`, `现金等价物的期末余额`, `现金等价物的期初余额`, `流动比率`, `速动比率`, `现金比率`, `负债权益比率`, `股东权益比率1`, `股东权益对负债比率`, `权益乘数`, `长期债务与营运资金比`, `长期负债比率1`, `利息支付倍数`, `股东权益与固定资产比`, `固定资产对长期负债比`, `有形净值债务率`, `清算价值比率`, `债务保障率`, `现金流量比率`, `每股有形资产净值`, `每股营运资金`, `债务总额EBITDA`, `营业周期`, `存货周转天数`, `应收账款周转天数`, `流动资产周转天数`, `总资产周转天数`, `存货周转率`, `应收账款周转率`, `流动资产周转率`, `固定资产周转率`, `总资产周转率`, `净资产周转率`, `股东权益周转率`, `营运资金周转率`, `存货同比增长率`, `应收帐款同比增长率`, `主营业务收入增长率`, `营业利润增长率`, `利润总额增长率`, `净利润增长率`, `净资产增长率`, `流动资产增长率`, `固定资产增长率`, `总资产增长率`, `摊薄每股收益增长率`, `每股净资产增长率`, `每股经营性现金流量增长率`, `三年平均净资收益率`, `总资产净利润率`, `投入资本回报率ROIC`, `成本费用利润率`, `营业利润率`, `主营业务成本率`, `销售净利率`, `总资产报酬率`, `销售毛利率`, `三项费用比重`, `营业费用率`, `管理费用率`, `财务费用率`, `非主营比重`, `营业利润比重`, `每股息税折旧摊销前利润`, `每股息税前利润EBIT`, `EBITDA主营业务收入`, `资产负债率`, `股东权益比率`, `长期负债比率`, `股东权益与固定资产比率`, `负债与所有者权益比率`, `长期资产与长期资金比率`, `资本化比率`, `资本固定化比率`, `固定资产比重`, `经营现金净流量对销售收入比率`, `资产的经营现金流量回报率`, `经营现金净流量与净利润的比率`, `经营现金净流量对负债比率`, `每股营业现金流量`, `每股经营活动现金流量净额`, `每股投资活动产生现金流量净额`, `每股筹资活动产生现金流量净额`, `每股现金及现金等价物净增加额`, `现金流量满足率`, `现金营运指数`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_param =tuple(list_data[i])
        with conn as con:
            try:
                con.execute(sql,sql_param)
            except Exception as e:
                errorlist.append(e)
                print(e)

    return errorlist


if __name__ == '__main__' :
    error = update_financial('20180101',conn=serverconn())