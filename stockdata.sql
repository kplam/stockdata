-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: 2017-12-03 11:46:09
-- 服务器版本： 5.7.19
-- PHP Version: 7.0.23

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stockdata`
--

-- --------------------------------------------------------

--
-- 表的结构 `basedata`
--

DROP TABLE IF EXISTS `basedata`;
CREATE TABLE IF NOT EXISTS `basedata` (
  `证券代码` varchar(30) NOT NULL,
  `证券简称` varchar(30) NOT NULL,
  `公司名称` longtext,
  `英文名称` longtext,
  `曾用名` longtext,
  `公司简介` longtext,
  `成立日期` date DEFAULT '1990-01-01',
  `工商登记号` varchar(30) DEFAULT NULL,
  `注册资本` varchar(30) DEFAULT NULL,
  `法人代表` longtext,
  `所属证监会行业` longtext,
  `员工总数` longtext,
  `总经理` varchar(30) DEFAULT NULL,
  `董事会秘书` varchar(30) DEFAULT NULL,
  `省份` varchar(30) DEFAULT NULL,
  `城市` varchar(30) DEFAULT NULL,
  `注册地址` longtext,
  `办公地址` longtext,
  `邮编` varchar(30) DEFAULT NULL,
  `电话` longtext,
  `传真` longtext,
  `电子邮件` longtext,
  `公司网站` longtext,
  `审计机构` longtext,
  `法律顾问` longtext,
  `经营分析` longtext,
  `简史` longtext,
  `核心题材` longtext,
  `所属主题` longtext,
  `所属概念` longtext,
  `首发日期` date DEFAULT '1990-01-01',
  `首发价格` float DEFAULT NULL,
  `更新日期` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `实际控制人名称` varchar(256) DEFAULT NULL,
  `实际控制人类型` varchar(128) DEFAULT NULL,
  `央企控制人名称` varchar(128) DEFAULT NULL,
  `控股股东名称` varchar(256) DEFAULT NULL,
  `控股股东类型` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`证券代码`),
  KEY `证券简称` (`证券简称`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 替换视图以便查看 `basedata search`
-- (See below for the actual view)
--
DROP VIEW IF EXISTS `basedata search`;
CREATE TABLE IF NOT EXISTS `basedata search` (
`证券简称` varchar(30)
,`证券代码` varchar(30)
,`公司简介` longtext
,`经营分析` longtext
,`简史` longtext
,`核心题材` longtext
,`所属主题` longtext
,`所属概念` longtext
);

-- --------------------------------------------------------

--
-- 表的结构 `blocktrade`
--

DROP TABLE IF EXISTS `blocktrade`;
CREATE TABLE IF NOT EXISTS `blocktrade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(63) NOT NULL,
  `name` varchar(63) DEFAULT NULL,
  `交易日期` date NOT NULL,
  `买方代码` varchar(63) DEFAULT NULL,
  `买方营业部` varchar(63) DEFAULT NULL,
  `收盘价` double DEFAULT NULL,
  `成交价` double DEFAULT NULL,
  `涨跌幅` double DEFAULT NULL,
  `卖方代码` varchar(63) DEFAULT NULL,
  `卖方营业部` varchar(63) DEFAULT NULL,
  `类型` varchar(63) DEFAULT NULL,
  `市场` varchar(63) DEFAULT NULL,
  `成交额` double DEFAULT NULL,
  `成交量` double DEFAULT NULL,
  `单位` varchar(63) DEFAULT NULL,
  `YSSLTAG` double DEFAULT NULL,
  PRIMARY KEY (`id`,`code`,`交易日期`),
  KEY `cdoe` (`code`,`买方营业部`,`卖方营业部`),
  KEY `类型` (`类型`)
) ENGINE=InnoDB AUTO_INCREMENT=172145 DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`交易日期`))
(
PARTITION p10 VALUES LESS THAN (2011) ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012) ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013) ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014) ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `capitalchange`
--

DROP TABLE IF EXISTS `capitalchange`;
CREATE TABLE IF NOT EXISTS `capitalchange` (
  `﻿股票代码` varchar(63) NOT NULL,
  `变动日期` date NOT NULL DEFAULT '1990-01-01',
  `变动原因` varchar(63) DEFAULT NULL,
  `总股本_变动` double DEFAULT NULL,
  `流通A股_变动` double DEFAULT NULL,
  `流通B股_变动` double DEFAULT NULL,
  `总股本_前值` double DEFAULT NULL,
  `流通A股_前值` double DEFAULT NULL,
  `流通B股_前值` double DEFAULT NULL,
  `总股本` double DEFAULT NULL,
  `流通A股` double DEFAULT NULL,
  `流通B股` double DEFAULT NULL,
  PRIMARY KEY (`﻿股票代码`,`变动日期`),
  KEY `变动日期` (`变动日期`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `cirholder`
--

DROP TABLE IF EXISTS `cirholder`;
CREATE TABLE IF NOT EXISTS `cirholder` (
  `code` varchar(12) NOT NULL,
  `date` date NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  `type` varchar(63) DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `abh` varchar(63) DEFAULT NULL,
  PRIMARY KEY (`code`,`date`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `dayline`
--

DROP TABLE IF EXISTS `dayline`;
CREATE TABLE IF NOT EXISTS `dayline` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `high` float NOT NULL,
  `open` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `vol` float NOT NULL,
  `amo` float NOT NULL,
  `adjfactor` float DEFAULT '1',
  `adjcump` float DEFAULT '1',
  PRIMARY KEY (`code`,`date`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p92 VALUES LESS THAN (1993) ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994) ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995) ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996) ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997) ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998) ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999) ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000) ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001) ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002) ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003) ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004) ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005) ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006) ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007) ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008) ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009) ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010) ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011) ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012) ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013) ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014) ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `dayline_tmp`
--

DROP TABLE IF EXISTS `dayline_tmp`;
CREATE TABLE IF NOT EXISTS `dayline_tmp` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `adjfactor` float DEFAULT '1',
  `adjcump` float DEFAULT '1',
  PRIMARY KEY (`code`,`date`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p92 VALUES LESS THAN (1993) ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994) ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995) ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996) ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997) ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998) ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999) ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000) ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001) ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002) ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003) ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004) ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005) ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006) ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007) ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008) ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009) ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010) ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011) ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012) ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013) ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014) ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

--
-- 触发器 `dayline_tmp`
--
DROP TRIGGER IF EXISTS `update_adjfactor_sync`;
DELIMITER $$
CREATE TRIGGER `update_adjfactor_sync` AFTER INSERT ON `dayline_tmp` FOR EACH ROW UPDATE `dayline`
SET 
`dayline`.`adjfactor`=NEW.`adjfactor`,
`dayline`.`adjcump`=NEW.`adjcump`
WHERE
`dayline`.`code`=NEW.`code` AND
`dayline`.`date`=NEW.`date`
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `faresult`
--

DROP TABLE IF EXISTS `faresult`;
CREATE TABLE IF NOT EXISTS `faresult` (
  `代码` varchar(63) DEFAULT NULL,
  `报表日期` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `favorite`
--

DROP TABLE IF EXISTS `favorite`;
CREATE TABLE IF NOT EXISTS `favorite` (
  `favorite_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `stock_code` varchar(30) NOT NULL,
  `stock_name` varchar(30) NOT NULL,
  `add_date` date NOT NULL,
  PRIMARY KEY (`favorite_id`)
) ENGINE=InnoDB AUTO_INCREMENT=598 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `financial`
--

DROP TABLE IF EXISTS `financial`;
CREATE TABLE IF NOT EXISTS `financial` (
  `名称` varchar(30) NOT NULL,
  `报表日期` date NOT NULL DEFAULT '1990-01-01',
  `代码` varchar(30) NOT NULL,
  `摊薄每股收益` float DEFAULT NULL,
  `净资产收益率` float DEFAULT NULL,
  `每股经营活动现金流量` float DEFAULT NULL,
  `每股净资产` float DEFAULT NULL,
  `每股资本公积金` float DEFAULT NULL,
  `每股未分配利润` float DEFAULT NULL,
  `每股主营收入` float DEFAULT NULL,
  `扣除非经常损益每股收益` float DEFAULT NULL,
  `货币资金` float DEFAULT NULL,
  `交易性金融资产` float DEFAULT NULL,
  `应收票据` float DEFAULT NULL,
  `应收账款` float DEFAULT NULL,
  `预付款项` float DEFAULT NULL,
  `应收利息` float DEFAULT NULL,
  `应收股利` float DEFAULT NULL,
  `其他应收款` float DEFAULT NULL,
  `应收关联公司款` float DEFAULT NULL,
  `存货` float DEFAULT NULL,
  `消耗性生物资产` float DEFAULT NULL,
  `一年内到期的非流动资产` float DEFAULT NULL,
  `其他流动资产` float DEFAULT NULL,
  `流动资产合计` float DEFAULT NULL,
  `可供出售金融资产` float DEFAULT NULL,
  `持有至到期投资` float DEFAULT NULL,
  `长期应收款` float DEFAULT NULL,
  `长期股权投资` float DEFAULT NULL,
  `投资性房地产` float DEFAULT NULL,
  `固定资产` float DEFAULT NULL,
  `在建工程` float DEFAULT NULL,
  `工程物资` float DEFAULT NULL,
  `固定资产清理` float DEFAULT NULL,
  `生产性生物资产` float DEFAULT NULL,
  `油气资产` float DEFAULT NULL,
  `无形资产` float DEFAULT NULL,
  `开发支出` float DEFAULT NULL,
  `商誉` float DEFAULT NULL,
  `长期待摊费用` float DEFAULT NULL,
  `递延所得税资产` float DEFAULT NULL,
  `其他非流动资产` float DEFAULT NULL,
  `非流动资产合计` float DEFAULT NULL,
  `资产总计` float DEFAULT NULL,
  `短期借款` float DEFAULT NULL,
  `交易性金融负债` float DEFAULT NULL,
  `应付票据` float DEFAULT NULL,
  `应付账款` float DEFAULT NULL,
  `预收账款` float DEFAULT NULL,
  `应付职工薪酬` float DEFAULT NULL,
  `应交税费` float DEFAULT NULL,
  `应付利息` float DEFAULT NULL,
  `应付股利` float DEFAULT NULL,
  `其他应付款` float DEFAULT NULL,
  `应付关联公司款` float DEFAULT NULL,
  `一年内到期的非流动负债` float DEFAULT NULL,
  `其他流动负债` float DEFAULT NULL,
  `流动负债合计` float DEFAULT NULL,
  `长期借款` float DEFAULT NULL,
  `应付债券` float DEFAULT NULL,
  `长期应付款` float DEFAULT NULL,
  `专项应付款` float DEFAULT NULL,
  `预计负债` float DEFAULT NULL,
  `递延所得税负债` float DEFAULT NULL,
  `其他非流动负债` float DEFAULT NULL,
  `非流动负债合计` float DEFAULT NULL,
  `负债合计` float DEFAULT NULL,
  `实收资本或股本` float DEFAULT NULL,
  `资本公积` float DEFAULT NULL,
  `库存股` float DEFAULT NULL,
  `盈余公积` float DEFAULT NULL,
  `未分配利润` float DEFAULT NULL,
  `外币报表折算差额` float DEFAULT NULL,
  `非正常经营项目收益调整` float DEFAULT NULL,
  `股东权益合计不含少数股东权益` float DEFAULT NULL,
  `少数股东权益` float DEFAULT NULL,
  `股东权益合计含少数股东权益` float DEFAULT NULL,
  `负债和股东权益合计` float DEFAULT NULL,
  `营业收入` float DEFAULT NULL,
  `营业成本` float DEFAULT NULL,
  `营业税金及附加` float DEFAULT NULL,
  `销售费用` float DEFAULT NULL,
  `管理费用` float DEFAULT NULL,
  `堪探费用` float DEFAULT NULL,
  `财务费用z` float DEFAULT NULL,
  `资产减值损失` float DEFAULT NULL,
  `公允价值变动净收益` float DEFAULT NULL,
  `投资收益` float DEFAULT NULL,
  `对联合营企业的投资收益` float DEFAULT NULL,
  `影响营业利润的其他科目` float DEFAULT NULL,
  `营业利润` float DEFAULT NULL,
  `补贴收入` float DEFAULT NULL,
  `营业外收入` float DEFAULT NULL,
  `营业外支出` float DEFAULT NULL,
  `非流动资产处置净损失` float DEFAULT NULL,
  `影响利润总额的其他科目` float DEFAULT NULL,
  `利润总额` float DEFAULT NULL,
  `所得税费用` float DEFAULT NULL,
  `影响净利润的其他科目` float DEFAULT NULL,
  `净利润含少数股东损益` float DEFAULT NULL,
  `净利润不含少数股东损益` float DEFAULT NULL,
  `少数股东损益` float DEFAULT NULL,
  `销售商品、提供劳务收到的现金` float DEFAULT NULL,
  `收到的税费返还` float DEFAULT NULL,
  `收到的其他与经营活动有关的现金` float DEFAULT NULL,
  `经营活动现金流入小计` float DEFAULT NULL,
  `购买商品、接受劳务支付的现金` float DEFAULT NULL,
  `支付给职工以及为职工支付的现金` float DEFAULT NULL,
  `支付的各项税费` float DEFAULT NULL,
  `支付的其他与经营活动有关的现金` float DEFAULT NULL,
  `经营活动现金流出小计` float DEFAULT NULL,
  `经营活动产生的现金流量净额` float DEFAULT NULL,
  `收回投资所收到的现金` float DEFAULT NULL,
  `取得投资收益所收到的现金` float DEFAULT NULL,
  `处置固定、无形和其他长期资产收回的现金净额` float DEFAULT NULL,
  `处置子公司及其他营业单位收到的现金净额` float DEFAULT NULL,
  `收到的其他与投资活动有关的现金` float DEFAULT NULL,
  `投资活动现金流入小计` float DEFAULT NULL,
  `购建固定资产、无形资产和其他长期资产支付的现金` float DEFAULT NULL,
  `投资所支付的现金` float DEFAULT NULL,
  `取得子公司及其他营业单位支付的现金净额` float DEFAULT NULL,
  `支付其他与投资活动有关的现金` float DEFAULT NULL,
  `投资活动现金流出小计` float DEFAULT NULL,
  `投资活动产生的现金流量净额` float DEFAULT NULL,
  `吸收投资所收到的现金` float DEFAULT NULL,
  `子公司吸收少数股东权益性投资收到的现金` float DEFAULT NULL,
  `取得借款收到的现金` float DEFAULT NULL,
  `收到其他与筹资活动有关的现金` float DEFAULT NULL,
  `筹资活动现金流入小计` float DEFAULT NULL,
  `偿还债务支付的现金` float DEFAULT NULL,
  `分配股利、利润或偿付利息支付的现金` float DEFAULT NULL,
  `子公司支给付少数股东的股利、利润` float DEFAULT NULL,
  `支付其他与筹资活动有关的现金` float DEFAULT NULL,
  `筹资活动现金流出小计` float DEFAULT NULL,
  `筹资活动产生的现金流量净额` float DEFAULT NULL,
  `汇率变动对现金的影响` float DEFAULT NULL,
  `其他原因对现金的影响` float DEFAULT NULL,
  `现金及现金等价物净增加额` float DEFAULT NULL,
  `期初现金及现金等价物余额` float DEFAULT NULL,
  `期末现金及现金等价物余额` float DEFAULT NULL,
  `净利润` float DEFAULT NULL,
  `加：资产减值准备` float DEFAULT NULL,
  `固定资产折旧、油气资产折耗、生产性生物资产折旧` float DEFAULT NULL,
  `无形资产摊销` float DEFAULT NULL,
  `长期待摊费用摊销` float DEFAULT NULL,
  `处置固定资产、无形资产和其他长期资产的损失` float DEFAULT NULL,
  `固定资产报废损失` float DEFAULT NULL,
  `公允价值变动损失` float DEFAULT NULL,
  `财务费用l` float DEFAULT NULL,
  `投资损失` float DEFAULT NULL,
  `递延所得税资产减少` float DEFAULT NULL,
  `递延所得税负债增加` float DEFAULT NULL,
  `存货的减少` float DEFAULT NULL,
  `经营性应收项目的减少` float DEFAULT NULL,
  `经营性应付项目的增加` float DEFAULT NULL,
  `其他` float DEFAULT NULL,
  `债务转为资本` float DEFAULT NULL,
  `一年内到期的可转换公司债券` float DEFAULT NULL,
  `融资租入固定资产` float DEFAULT NULL,
  `现金的期末余额` float DEFAULT NULL,
  `现金的期初余额` float DEFAULT NULL,
  `现金等价物的期末余额` float DEFAULT NULL,
  `现金等价物的期初余额` float DEFAULT NULL,
  `流动比率` float DEFAULT NULL,
  `速动比率` float DEFAULT NULL,
  `现金比率` float DEFAULT NULL,
  `负债权益比率` float DEFAULT NULL,
  `股东权益比率1` float DEFAULT NULL,
  `股东权益对负债比率` float DEFAULT NULL,
  `权益乘数` float DEFAULT NULL,
  `长期债务与营运资金比` float DEFAULT NULL,
  `长期负债比率1` float DEFAULT NULL,
  `利息支付倍数` float DEFAULT NULL,
  `股东权益与固定资产比` float DEFAULT NULL,
  `固定资产对长期负债比` float DEFAULT NULL,
  `有形净值债务率` float DEFAULT NULL,
  `清算价值比率` float DEFAULT NULL,
  `债务保障率` float DEFAULT NULL,
  `现金流量比率` float DEFAULT NULL,
  `每股有形资产净值` float DEFAULT NULL,
  `每股营运资金` float DEFAULT NULL,
  `债务总额EBITDA` float DEFAULT NULL,
  `营业周期` float DEFAULT NULL,
  `存货周转天数` float DEFAULT NULL,
  `应收账款周转天数` float DEFAULT NULL,
  `流动资产周转天数` float DEFAULT NULL,
  `总资产周转天数` float DEFAULT NULL,
  `存货周转率` float DEFAULT NULL,
  `应收账款周转率` float DEFAULT NULL,
  `流动资产周转率` float DEFAULT NULL,
  `固定资产周转率` float DEFAULT NULL,
  `总资产周转率` float DEFAULT NULL,
  `净资产周转率` float DEFAULT NULL,
  `股东权益周转率` float DEFAULT NULL,
  `营运资金周转率` float DEFAULT NULL,
  `存货同比增长率` float DEFAULT NULL,
  `应收帐款同比增长率` float DEFAULT NULL,
  `主营业务收入增长率` float DEFAULT NULL,
  `营业利润增长率` float DEFAULT NULL,
  `利润总额增长率` float DEFAULT NULL,
  `净利润增长率` float DEFAULT NULL,
  `净资产增长率` float DEFAULT NULL,
  `流动资产增长率` float DEFAULT NULL,
  `固定资产增长率` float DEFAULT NULL,
  `总资产增长率` float DEFAULT NULL,
  `摊薄每股收益增长率` float DEFAULT NULL,
  `每股净资产增长率` float DEFAULT NULL,
  `每股经营性现金流量增长率` float DEFAULT NULL,
  `三年平均净资收益率` float DEFAULT NULL,
  `总资产净利润率` float DEFAULT NULL,
  `投入资本回报率ROIC` float DEFAULT NULL,
  `成本费用利润率` float DEFAULT NULL,
  `营业利润率` float DEFAULT NULL,
  `主营业务成本率` float DEFAULT NULL,
  `销售净利率` float DEFAULT NULL,
  `总资产报酬率` float DEFAULT NULL,
  `销售毛利率` float DEFAULT NULL,
  `三项费用比重` float DEFAULT NULL,
  `营业费用率` float DEFAULT NULL,
  `管理费用率` float DEFAULT NULL,
  `财务费用率` float DEFAULT NULL,
  `非主营比重` float DEFAULT NULL,
  `营业利润比重` float DEFAULT NULL,
  `每股息税折旧摊销前利润` float DEFAULT NULL,
  `每股息税前利润EBIT` float DEFAULT NULL,
  `EBITDA主营业务收入` float DEFAULT NULL,
  `资产负债率` float DEFAULT NULL,
  `股东权益比率` float DEFAULT NULL,
  `长期负债比率` float DEFAULT NULL,
  `股东权益与固定资产比率` float DEFAULT NULL,
  `负债与所有者权益比率` float DEFAULT NULL,
  `长期资产与长期资金比率` float DEFAULT NULL,
  `资本化比率` float DEFAULT NULL,
  `资本固定化比率` float DEFAULT NULL,
  `固定资产比重` float DEFAULT NULL,
  `经营现金净流量对销售收入比率` float DEFAULT NULL,
  `资产的经营现金流量回报率` float DEFAULT NULL,
  `经营现金净流量与净利润的比率` float DEFAULT NULL,
  `经营现金净流量对负债比率` float DEFAULT NULL,
  `每股营业现金流量` float DEFAULT NULL,
  `每股经营活动现金流量净额` float DEFAULT NULL,
  `每股投资活动产生现金流量净额` float DEFAULT NULL,
  `每股筹资活动产生现金流量净额` float DEFAULT NULL,
  `每股现金及现金等价物净增加额` float DEFAULT NULL,
  `现金流量满足率` float DEFAULT NULL,
  `现金营运指数` float DEFAULT NULL,
  PRIMARY KEY (`报表日期`,`代码`),
  KEY `代码` (`代码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`报表日期`))
(
PARTITION p92 VALUES LESS THAN (1993) ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994) ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995) ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996) ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997) ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998) ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999) ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000) ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001) ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002) ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003) ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004) ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005) ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006) ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007) ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008) ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009) ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010) ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011) ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012) ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013) ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014) ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `forecast`
--

DROP TABLE IF EXISTS `forecast`;
CREATE TABLE IF NOT EXISTS `forecast` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `业绩变动` longtext NOT NULL,
  `变动幅度` longtext NOT NULL,
  `预告类型` varchar(30) NOT NULL,
  `同期净利润` double NOT NULL,
  `财报日期` date NOT NULL DEFAULT '1990-01-01',
  PRIMARY KEY (`code`,`date`,`财报日期`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ftsplit`
--

DROP TABLE IF EXISTS `ftsplit`;
CREATE TABLE IF NOT EXISTS `ftsplit` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `红股` float DEFAULT '0',
  `配股` float DEFAULT '0',
  `配股价` float DEFAULT '0',
  `红利` float DEFAULT '0',
  `前收盘价` float DEFAULT '0',
  `除权价` float DEFAULT '0',
  `单次复权因子` float DEFAULT '1',
  `累计复权因子` float DEFAULT '1',
  PRIMARY KEY (`code`,`date`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indexdb`
--

DROP TABLE IF EXISTS `indexdb`;
CREATE TABLE IF NOT EXISTS `indexdb` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `high` float NOT NULL,
  `open` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `vol` float NOT NULL,
  `amo` float NOT NULL,
  PRIMARY KEY (`code`,`date`),
  KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indexlist`
--

DROP TABLE IF EXISTS `indexlist`;
CREATE TABLE IF NOT EXISTS `indexlist` (
  `code` varchar(30) NOT NULL,
  `market` varchar(30) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `short` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indicator`
--

DROP TABLE IF EXISTS `indicator`;
CREATE TABLE IF NOT EXISTS `indicator` (
  `name` varchar(60) NOT NULL,
  `short` varchar(30) NOT NULL,
  `input` longtext NOT NULL,
  `output` longtext NOT NULL,
  `main` tinyint(1) DEFAULT '0',
  UNIQUE KEY `short` (`short`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `lhb`
--

DROP TABLE IF EXISTS `lhb`;
CREATE TABLE IF NOT EXISTS `lhb` (
  `index` int(2) NOT NULL,
  `date` date NOT NULL,
  `code` varchar(12) NOT NULL,
  `买入金额` double DEFAULT NULL,
  `卖出金额` double DEFAULT NULL,
  `净买入金额` double DEFAULT NULL,
  `净买入金额占总成交额` float DEFAULT NULL,
  `pl` varchar(63) DEFAULT NULL,
  `上榜原因` varchar(256) NOT NULL,
  `买卖方向` int(2) NOT NULL,
  `营业部代码` varchar(63) NOT NULL,
  `营业部名称` varchar(256) DEFAULT NULL,
  `买入金额占总成交额` double DEFAULT NULL,
  `卖出金额占总成交额` double DEFAULT NULL,
  `上榜总成交额` double DEFAULT NULL,
  PRIMARY KEY (`index`,`date`,`code`,`上榜原因`),
  KEY `营业部名称` (`营业部名称`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `news`
--

DROP TABLE IF EXISTS `news`;
CREATE TABLE IF NOT EXISTS `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` text NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `title` text,
  `link` varchar(256) NOT NULL,
  `content` longtext,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `link` (`link`),
  KEY `type` (`type`),
  KEY `datetime` (`datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=567705 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `shareholder`
--

DROP TABLE IF EXISTS `shareholder`;
CREATE TABLE IF NOT EXISTS `shareholder` (
  `code` varchar(12) NOT NULL,
  `date` date NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  `quantity` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `type` varchar(63) DEFAULT NULL,
  PRIMARY KEY (`code`,`date`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `stocklist`
--

DROP TABLE IF EXISTS `stocklist`;
CREATE TABLE IF NOT EXISTS `stocklist` (
  `证券代码` varchar(30) NOT NULL,
  `证券简称` longtext NOT NULL,
  `上市市场` varchar(30) DEFAULT NULL,
  `交易状态` int(1) NOT NULL DEFAULT '1',
  `拼音缩写` varchar(8) NOT NULL,
  PRIMARY KEY (`证券代码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `stocklist`
--
DROP TRIGGER IF EXISTS `after_insert_on_stocklist`;
DELIMITER $$
CREATE TRIGGER `after_insert_on_stocklist` AFTER INSERT ON `stocklist` FOR EACH ROW INSERT
INTO
  `basedata`(`证券代码`,
  `证券简称`)
VALUES(NEW.`证券代码`, NEW.`证券简称`)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `after_update_on_stocklist`;
DELIMITER $$
CREATE TRIGGER `after_update_on_stocklist` AFTER UPDATE ON `stocklist` FOR EACH ROW UPDATE `basedata` SET `证券简称`=NEW.`证券简称` WHERE `basedata`.`证券代码`=NEW.`证券代码`
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `tmp`
--

DROP TABLE IF EXISTS `tmp`;
CREATE TABLE IF NOT EXISTS `tmp` (
  `code` varchar(63) NOT NULL,
  `date` date NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `tmp`
--
DROP TRIGGER IF EXISTS `precentage_sync`;
DELIMITER $$
CREATE TRIGGER `precentage_sync` AFTER INSERT ON `tmp` FOR EACH ROW UPDATE `usefuldata`
SET
`usefuldata`.`precentage` = New.`percentage`
WHERE
`usefuldata`.`code`=NEW.`code` and `usefuldata`.`date`=NEW.`date`
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `usefuldata`
--

DROP TABLE IF EXISTS `usefuldata`;
CREATE TABLE IF NOT EXISTS `usefuldata` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `AmoRank` int(11) DEFAULT NULL,
  `ARaise` int(11) DEFAULT NULL,
  `precentage` float DEFAULT NULL,
  `涨跌动因` varchar(256) NOT NULL DEFAULT '',
  `taresult` varchar(30) DEFAULT '0',
  PRIMARY KEY (`code`,`date`),
  KEY `date` (`date`),
  KEY `ARaise` (`ARaise`),
  KEY `taresult` (`taresult`),
  KEY `AmoRank` (`AmoRank`),
  KEY `precentage` (`precentage`),
  KEY `涨跌动因` (`涨跌动因`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p92 VALUES LESS THAN (1993) ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994) ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995) ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996) ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997) ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998) ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999) ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000) ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001) ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002) ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003) ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004) ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005) ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006) ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007) ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008) ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009) ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010) ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011) ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012) ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013) ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014) ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015) ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016) ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017) ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018) ENGINE=InnoDB,
PARTITION p0000 VALUES LESS THAN MAXVALUE ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_login_id` varchar(32) NOT NULL,
  `user_password` varchar(512) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `user_email` text NOT NULL,
  `user_mobile` varchar(11) NOT NULL,
  `user_group` varchar(15) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 视图结构 `basedata search`
--
DROP TABLE IF EXISTS `basedata search`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `basedata search`  AS  (select `basedata`.`证券简称` AS `证券简称`,`basedata`.`证券代码` AS `证券代码`,`basedata`.`公司简介` AS `公司简介`,`basedata`.`经营分析` AS `经营分析`,`basedata`.`简史` AS `简史`,`basedata`.`核心题材` AS `核心题材`,`basedata`.`所属主题` AS `所属主题`,`basedata`.`所属概念` AS `所属概念` from `basedata`) ;

--
-- 限制导出的表
--

--
-- 限制表 `basedata`
--
ALTER TABLE `basedata`
  ADD CONSTRAINT `basedata_ibfk_1` FOREIGN KEY (`证券代码`) REFERENCES `stocklist` (`证券代码`);
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
