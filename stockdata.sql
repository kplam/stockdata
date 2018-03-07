-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2018-03-01 14:50:28
-- 服务器版本： 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stockdata`
--

DELIMITER $$
--
-- 函数
--
CREATE DEFINER=`root`@`%` FUNCTION `getPY` (`in_string` VARCHAR(21845)) RETURNS MEDIUMTEXT CHARSET utf8 BEGIN
DECLARE tmp_str VARCHAR(21845) charset gbk DEFAULT '' ; #截取字符串，每次做截取后的字符串存放在该变量中，初始为函数参数in_string值 
DECLARE tmp_len SMALLINT DEFAULT 0;#tmp_str的长度 
DECLARE tmp_char VARCHAR(2) charset gbk DEFAULT '';#截取字符，每次 left(tmp_str,1) 返回值存放在该变量中 
DECLARE tmp_rs VARCHAR(21845) charset gbk DEFAULT '';#结果字符串 
DECLARE tmp_cc VARCHAR(2) charset gbk DEFAULT '';#拼音字符，存放单个汉字对应的拼音首字符 
DECLARE tmp_rsd VARCHAR(21845) CHARSET gbk DEFAULT '';
SET tmp_str = in_string;#初始化，将in_string赋给tmp_str 
SET tmp_len = LENGTH(tmp_str);#初始化长度 
IF POSITION('银行' IN tmp_str)!=0 THEN
SELECT REPLACE(tmp_str,'银行','YH') INTO tmp_str;
END IF;
WHILE tmp_len > 0 DO #如果被计算的tmp_str长度大于0则进入该while 
SET tmp_char = LEFT(tmp_str,1);#获取tmp_str最左端的首个字符，注意这里是获取首个字符，该字符可能是汉字，也可能不是。 
SET tmp_cc = tmp_char;#左端首个字符赋值给拼音字符 
IF LENGTH(tmp_char)>1 THEN#判断左端首个字符是多字节还是单字节字符，要是多字节则认为是汉字且作以下拼音获取，要是单字节则不处理。 
SELECT ELT(INTERVAL(CONV(HEX(tmp_char),16,10),0xB0A1,0xB0C5,0xB2C1,0xB4EE,0xB6EA,0xB7A2,0xB8C1,0xB9FE,0xBBF7,0xBFA6,0xC0AC 
,0xC2E8,0xC4C3,0xC5B6,0xC5BE,0xC6DA,0xC8BB,0xC8F6,0xCBFA,0xCDDA ,0xCEF4,0xD1B9,0xD4D1), 
'A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','W','X','Y','Z') INTO tmp_cc; #获得汉字拼音首字符 
END IF; 
SET tmp_rs = CONCAT(tmp_rs,tmp_cc);#将当前tmp_str左端首个字符拼音首字符与返回字符串拼接 
SET tmp_str = SUBSTRING(tmp_str,2);#将tmp_str左端首字符去除 
SET tmp_len = LENGTH(tmp_str);#计算当前字符串长度 
END WHILE; 
RETURN tmp_rs;#返回结果字符串 
END$$

CREATE DEFINER=`root`@`%` FUNCTION `test` (`in_string` VARCHAR(21845)) RETURNS MEDIUMTEXT CHARSET utf8 BEGIN
DECLARE tmp_str VARCHAR(21845) CHARSET gbk DEFAULT '' ; #截取字符串，每次做截取后的字符串存放在该变量中，初始为函数参数in_string值 
DECLARE tmp_len SMALLINT DEFAULT 0;#tmp_str的长度 
DECLARE tmp_char VARCHAR(2) CHARSET gbk DEFAULT '';#截取字符，每次 left(tmp_str,1) 返回值存放在该变量中 
DECLARE tmp_rs VARCHAR(21845) CHARSET gbk DEFAULT '';#结果字符串 
DECLARE tmp_cc VARCHAR(2) CHARSET gbk DEFAULT '';#拼音字符，存放单个汉字对应的拼音首字符 
DECLARE tmp_rsd VARCHAR(21845) CHARSET gbk DEFAULT '';
SET tmp_str = in_string;#初始化，将in_string赋给tmp_str 
SET tmp_len = LENGTH(tmp_str);#初始化长度 
IF POSITION('银行' IN tmp_str)!=0 THEN
SELECT REPLACE(tmp_str,'银行','YH') INTO tmp_rsd;
ELSE SET tmp_rsd = '银行';
END IF;
RETURN tmp_rsd;#返回结果字符串 
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `5min`
--

CREATE TABLE `5min` (
  `code` varchar(6) NOT NULL,
  `datetime` datetime NOT NULL,
  `open` float NOT NULL,
  `high` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `vol` float NOT NULL,
  `amo` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `basedata`
--

CREATE TABLE `basedata` (
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
  `所属证监会行业` enum('交通运输、仓储和邮政业','住宿和餐饮业','信息传输、软件和信息技术服务业','农、林、牧、渔业','制造业','卫生和社会工作','建筑业','房地产业','批发和零售业','教育','文化、体育和娱乐业','水利、环境和公共设施管理业','电力、热力、燃气及水生产和供应业','科学研究和技术服务业','租赁和商务服务业','综合','采矿业','金融业','居民服务、修理和其他服务业') DEFAULT NULL,
  `员工总数` longtext,
  `总经理` varchar(30) DEFAULT NULL,
  `董事会秘书` varchar(30) DEFAULT NULL,
  `省份` enum('上海','云南','内蒙古','北京','吉林','四川','天津','宁夏','安徽','山东','山西','广东','广西','新疆','江苏','江西','河北','河南','浙江','海南','湖北','湖南','甘肃','福建','西藏','贵州','辽宁','重庆','陕西','青海','黑龙江') DEFAULT NULL,
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
  `实际控制人类型` enum('','信托投资公司','其它','其它,其它金融公司,投资公司','其它,投资公司','其它,自然人','国务院所属部委','国务院直属事业单位','国务院直属机构','国务院直属特设机构','地方各级人民政府','地方所属部委','地方政府国有资产管理机构','地方政府国有资产管理机构,投资公司','地方政府财政部门','基金会','投资公司','投资公司,自然人','无控制人','自然人','资产管理公司','金融控股集团','高等院校') DEFAULT NULL,
  `央企控制人名称` varchar(128) DEFAULT NULL,
  `控股股东名称` varchar(256) DEFAULT NULL,
  `控股股东类型` enum('','信托投资公司','其它','其它,投资公司','其它,投资公司,自然人','其它,投资公司,资产管理公司','其它,自然人','其它金融公司','创业投资公司','创业投资公司,投资公司','国务院直属事业单位','地方政府国有资产管理机构','地方政府财政部门','基金管理公司','投资公司','投资公司,自然人','无控制人','综合保险公司','自然人','资产管理公司','金融控股集团','高等院校') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `basedata`
--
DELIMITER $$
CREATE TRIGGER `update_stocklist` AFTER UPDATE ON `basedata` FOR EACH ROW update `stocklist` set `stocklist`.`证券简称`=new.`证券简称`,`stocklist`.`拼音缩写`=getPY(new.`证券简称`) WHERE `stocklist`.`证券代码`=new.`证券代码`
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `blocktrade`
--

CREATE TABLE `blocktrade` (
  `id` int(11) NOT NULL,
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
  `类型` enum('BD0','EQA','EQB') DEFAULT NULL,
  `市场` enum('CNSESH','CNSESZ') DEFAULT NULL,
  `成交额` double DEFAULT NULL,
  `成交量` double DEFAULT NULL,
  `单位` enum('万手','万股') DEFAULT NULL,
  `YSSLTAG` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`交易日期`))
(
PARTITION p10 VALUES LESS THAN (2011)ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012)ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013)ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014)ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `blog`
--

CREATE TABLE `blog` (
  `id` int(11) NOT NULL,
  `type` varchar(32) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `author` varchar(32) DEFAULT NULL,
  `content` longtext,
  `lastupdate` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `buyback`
--

CREATE TABLE `buyback` (
  `证劵代码` varchar(12) NOT NULL,
  `方案进度` enum('完成','实施','未通过','股东大会通过','董事会通过') NOT NULL,
  `董事会通过日` date NOT NULL,
  `股东大会通过日` date DEFAULT NULL,
  `国资委通过日` date DEFAULT NULL,
  `证监会通过日` date DEFAULT NULL,
  `回购资金上限_CNY` double DEFAULT NULL,
  `回购价格上限_CNY` float DEFAULT NULL,
  `回购股份预计_万` double DEFAULT NULL,
  `占总股本` float DEFAULT NULL,
  `占实际流通股` float DEFAULT NULL,
  `股份种类` enum('A股','社会公众股','股权激励限售股') NOT NULL,
  `回购资金来源` enum('','自有资金','自有资金,自筹资金','自筹资金') DEFAULT NULL,
  `回购股份方式` enum('定向回购','集中竞价交易') DEFAULT NULL,
  `回购股份实施期限` varchar(63) DEFAULT NULL,
  `备注` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `capitalchange`
--

CREATE TABLE `capitalchange` (
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
  `流通B股` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `cirholder`
--

CREATE TABLE `cirholder` (
  `code` varchar(12) NOT NULL,
  `date` date NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  `type` enum('QFII','个人','企业年金','保险产品','保险公司','信托投资公司','信托计划','全国社保基金','其它','基本养老基金','基金管理公司','基金资产管理计划','投资公司','证券公司','证券投资基金','财务公司','金融','集合理财计划','高校') DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `abh` enum('A股','A股,B股','A股,H股','A股,S股','B股','B股,H股','H股','H股,A股','H股,B股','S股','不详') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `dayline`
--

CREATE TABLE `dayline` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `high` float NOT NULL,
  `open` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `vol` float NOT NULL,
  `amo` float NOT NULL,
  `adjfactor` float DEFAULT '1',
  `adjcump` float DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p92 VALUES LESS THAN (1993)ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994)ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995)ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996)ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997)ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998)ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999)ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000)ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001)ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002)ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003)ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004)ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005)ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006)ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007)ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008)ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009)ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010)ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011)ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012)ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013)ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014)ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `dayline_tmp`
--

CREATE TABLE `dayline_tmp` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `adjfactor` float DEFAULT '1',
  `adjcump` float DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `dayline_tmp`
--
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

CREATE TABLE `faresult` (
  `代码` varchar(63) DEFAULT NULL,
  `报表日期` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `favorite`
--

CREATE TABLE `favorite` (
  `favorite_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `stock_code` varchar(30) NOT NULL,
  `stock_name` varchar(30) NOT NULL,
  `add_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `financial`
--

CREATE TABLE `financial` (
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
  `现金营运指数` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`报表日期`))
(
PARTITION p92 VALUES LESS THAN (1993)ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994)ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995)ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996)ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997)ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998)ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999)ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000)ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001)ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002)ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003)ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004)ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005)ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006)ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007)ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008)ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009)ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010)ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011)ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012)ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013)ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014)ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `financial_rank`
--

CREATE TABLE `financial_rank` (
  `代码` varchar(63) NOT NULL,
  `名称` varchar(63) DEFAULT NULL,
  `报表日期` date NOT NULL,
  `可持续评分` float DEFAULT NULL,
  `成长评分` float DEFAULT NULL,
  `稳定性评分` float DEFAULT NULL,
  `产品评分` float DEFAULT NULL,
  `经营评分` float DEFAULT NULL,
  `收款评分` float DEFAULT NULL,
  `资产评分` float DEFAULT NULL,
  `总评分` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `forecast`
--

CREATE TABLE `forecast` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `业绩变动` longtext NOT NULL,
  `变动幅度` longtext NOT NULL,
  `预告类型` enum('','减亏','持平','预亏','预减','预增','预盈') NOT NULL,
  `同期净利润` double NOT NULL,
  `财报日期` date NOT NULL DEFAULT '1990-01-01',
  `上限` float DEFAULT NULL,
  `下限` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ftsplit`
--

CREATE TABLE `ftsplit` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `红股` float DEFAULT '0',
  `配股` float DEFAULT '0',
  `配股价` float DEFAULT '0',
  `红利` float DEFAULT '0',
  `前收盘价` float DEFAULT '0',
  `除权价` float DEFAULT '0',
  `单次复权因子` float DEFAULT '1',
  `累计复权因子` float DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `incentive`
--

CREATE TABLE `incentive` (
  `股票代码` varchar(12) NOT NULL,
  `本期计划制定年度` varchar(63) DEFAULT NULL,
  `本期计划激励次数` varchar(63) DEFAULT NULL,
  `方案进度` enum('停止实施','取消方案','实施','实施完成','未通过','股东大会通过','董事会预案') DEFAULT NULL,
  `激励标的物` enum('股票增值权','股票期权','限制性股票') NOT NULL,
  `标的股票来源` varchar(128) DEFAULT NULL,
  `激励总数_万` float DEFAULT NULL,
  `激励总数占当时总股本的比例` float DEFAULT NULL,
  `计划授权授予股票价格` float DEFAULT NULL,
  `本期计划有效期_年` int(2) DEFAULT NULL,
  `股权激励授予条件说明` longtext,
  `薪酬委员会预案公告日` date NOT NULL,
  `董事会修订方案日` date DEFAULT NULL,
  `股东大会通过日` date DEFAULT NULL,
  `独立财务顾问` varchar(63) DEFAULT NULL,
  `律师事务所` varchar(63) DEFAULT NULL,
  `备注` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indexdb`
--

CREATE TABLE `indexdb` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `high` float NOT NULL,
  `open` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `vol` float NOT NULL,
  `amo` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indexlist`
--

CREATE TABLE `indexlist` (
  `code` varchar(30) NOT NULL,
  `market` varchar(30) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `short` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `indicator`
--

CREATE TABLE `indicator` (
  `name` varchar(60) NOT NULL,
  `short` varchar(30) NOT NULL,
  `input` longtext NOT NULL,
  `output` longtext NOT NULL,
  `main` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `institutional`
--

CREATE TABLE `institutional` (
  `code` varchar(12) NOT NULL,
  `date` date NOT NULL,
  `fundcode` varchar(16) NOT NULL,
  `fundname` varchar(128) DEFAULT NULL,
  `type` enum('QFII','保险','信托','券商','基金','社保') DEFAULT NULL,
  `vol` int(16) DEFAULT NULL,
  `amo` double DEFAULT NULL,
  `percent` double DEFAULT NULL,
  `percent_cir` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p12 VALUES LESS THAN (2013)ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014)ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `lhb`
--

CREATE TABLE `lhb` (
  `index` int(2) NOT NULL,
  `date` date NOT NULL,
  `code` varchar(12) NOT NULL,
  `买入金额` double DEFAULT NULL,
  `卖出金额` double DEFAULT NULL,
  `净买入金额` double DEFAULT NULL,
  `净买入金额占总成交额` float DEFAULT NULL,
  `pl` varchar(63) DEFAULT NULL,
  `上榜原因` enum('单只标的证券的当日融资买入数量达到当日该证券总交易量的50%以上的证券','无价格涨跌幅限制的证券','日振幅值达15%的前三只证券|前五只证券','日换手率达20%的前三只证券|前五只证券','日涨幅偏离值达7%的前三只证券|前五只证券','日跌幅偏离值达7%的前三只证券|前五只证券','连续三个交易日内,日均换手率与前五个交易日的日均换手率的比值达到30倍,且换手率累计达20%的证券','连续三个交易日内,涨幅偏离值累计达12%的ST、*ST证券和S证券','连续三个交易日内,涨幅偏离值累计达15%的ST和*ST证券','连续三个交易日内,涨幅偏离值累计达20%的证券','连续三个交易日内,跌幅偏离值累计达12%的ST、*ST证券和S证券','连续三个交易日内,跌幅偏离值累计达15%的ST和*ST证券','连续三个交易日内,跌幅偏离值累计达20%的证券','退市整理的证券','风险警示股票盘中换手率达到或超过30%的证券') NOT NULL,
  `买卖方向` enum('1','2') NOT NULL,
  `营业部代码` varchar(63) NOT NULL,
  `营业部名称` varchar(256) DEFAULT NULL,
  `买入金额占总成交额` double DEFAULT NULL,
  `卖出金额占总成交额` double DEFAULT NULL,
  `上榜总成交额` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `lhb_base`
--

CREATE TABLE `lhb_base` (
  `营业部代码` varchar(63) NOT NULL,
  `级别` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `mainbusiness`
--

CREATE TABLE `mainbusiness` (
  `code` varchar(63) NOT NULL,
  `报表日期` date NOT NULL,
  `主营构成` varchar(63) NOT NULL,
  `主营收入` double DEFAULT NULL,
  `收入比例` float DEFAULT NULL,
  `主营成本` double DEFAULT NULL,
  `成本比例` float DEFAULT NULL,
  `主营利润` double DEFAULT NULL,
  `利润比例` float DEFAULT NULL,
  `毛利率` float DEFAULT NULL,
  `分类` enum('产品','行业','地区','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`报表日期`))
(
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `managerial`
--

CREATE TABLE `managerial` (
  `code` char(6) NOT NULL,
  `日期` date NOT NULL,
  `变动人` varchar(128) NOT NULL,
  `持股种类` enum('A股','H股') NOT NULL,
  `变动股数` bigint(20) NOT NULL,
  `变动后持股数` bigint(20) NOT NULL,
  `成交均价` float NOT NULL,
  `变动人与董监高的关系` enum('兄弟姐妹','其他组织','受控法人','子女','本人','父母','配偶') NOT NULL,
  `变动方式` varchar(128) NOT NULL,
  `变动金额` float NOT NULL,
  `职务` varchar(63) NOT NULL,
  `变动比例` decimal(10,8) NOT NULL,
  `董监高人员姓名` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`日期`))
(
PARTITION p05 VALUES LESS THAN (2010)ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2025)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `news`
--

CREATE TABLE `news` (
  `id` int(11) NOT NULL,
  `source` enum('stcn.com','zf826.com','55188.com') NOT NULL,
  `type` enum('【中签号查询】','【公司】','【其他】','【创投】','【数据】','【新三板】','【新股日历】','【最新股价】','【机构新闻】','【海外】','【港股】','【看点数据】','【财经新闻】','【资金流向】','【早知道】') DEFAULT NULL,
  `title` text,
  `link` varchar(256) NOT NULL,
  `content` longtext,
  `datetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `notice`
--

CREATE TABLE `notice` (
  `date` date NOT NULL,
  `title` varchar(256) DEFAULT NULL,
  `infocode` varchar(63) NOT NULL,
  `eutime` datetime DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `code` varchar(12) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `security_type` enum('A股','B股','H股','债券','非H股') DEFAULT NULL,
  `market` enum('上交所主板','上交所风险警示板','上海证券交易所','中国银行间市场','深交所中小板','深交所主板','深交所创业板','深交所风险警示板','深圳证券交易所','香港交易所主板') DEFAULT NULL,
  `type` varchar(63) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `realtimecal`
--

CREATE TABLE `realtimecal` (
  `id` int(11) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `taresult` longtext,
  `finalresult` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `refinance`
--

CREATE TABLE `refinance` (
  `股票代码` varchar(20) DEFAULT NULL,
  `融资类型` varchar(63) DEFAULT NULL,
  `最新公告日期` date DEFAULT NULL,
  `方案进度` varchar(63) DEFAULT NULL,
  `拟发行数量_万` float DEFAULT NULL,
  `拟发行价格` float DEFAULT NULL,
  `定价方式` varchar(63) DEFAULT NULL,
  `发行对象` text,
  `拟募集资金_万` float DEFAULT NULL,
  `主承销商` varchar(63) DEFAULT NULL,
  `首次公告日期` date DEFAULT NULL,
  `方案有效期` varchar(63) DEFAULT NULL,
  `董事会审议日` date DEFAULT NULL,
  `股东大会通过日` date DEFAULT NULL,
  `发审委通过日` date DEFAULT NULL,
  `证监会核准发行起始日` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `shareholder`
--

CREATE TABLE `shareholder` (
  `code` varchar(12) NOT NULL,
  `date` date NOT NULL,
  `rank` bigint(20) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  `quantity` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `change` double DEFAULT NULL,
  `type` enum('其他未流通股','其它未流通股','国家股','境内法人股','境外法人股','流通A股','流通A股,流通B股','流通A股,流通B股,限售流通A股,流通B股','流通A股,流通H股','流通A股,流通H股,限售流通A股,流通H股','流通A股,流通S股','流通A股,限售流通A股','流通B股','流通B股,流通H股','流通B股,限售流通B股','流通H股','流通H股,限售流通H股','流通S股','限售国家股','限售境内法人股','限售境外法人股','限售流通A股','限售流通H股') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `shareholdernumber`
--

CREATE TABLE `shareholdernumber` (
  `code` varchar(63) NOT NULL,
  `date` date NOT NULL,
  `close` float DEFAULT NULL,
  `scr` enum('NULL','较分散','较集中','非常分散','非常集中') DEFAULT NULL,
  `top10` float DEFAULT NULL,
  `cirtop10` float DEFAULT NULL,
  `shareholders` int(16) DEFAULT NULL,
  `shschange` float DEFAULT NULL,
  `avgamount` int(16) DEFAULT NULL,
  `avgcirquantity` float DEFAULT NULL,
  `avgcirchange` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (year(`date`))
(
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB,
PARTITION P30 VALUES LESS THAN (2031)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `spo_done`
--

CREATE TABLE `spo_done` (
  `code` varchar(12) NOT NULL,
  `name` varchar(12) NOT NULL,
  `发行方式` enum('公开增发','定向增发') DEFAULT NULL,
  `发行总数` bigint(20) NOT NULL,
  `发行价格` float DEFAULT NULL,
  `发行日期` date NOT NULL,
  `增发上市日期` date DEFAULT NULL,
  `增发代码` char(12) DEFAULT NULL,
  `网上发行` varchar(63) DEFAULT NULL,
  `中签号公布日` varchar(12) DEFAULT NULL,
  `中签率` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `statistics`
--

CREATE TABLE `statistics` (
  `date` date NOT NULL,
  `ontrade` int(5) NOT NULL,
  `halt` int(5) NOT NULL,
  `total` int(5) NOT NULL,
  `delisted` int(5) NOT NULL,
  `all_listed` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `stocklist`
--

CREATE TABLE `stocklist` (
  `证券代码` varchar(30) NOT NULL,
  `证券简称` longtext NOT NULL,
  `上市市场` enum('上海证券交易所','深圳证券交易所') NOT NULL,
  `交易状态` enum('0','1','9','-1') NOT NULL DEFAULT '1',
  `拼音缩写` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `stocklist`
--
DELIMITER $$
CREATE TRIGGER `after_insert_on_stocklist` AFTER INSERT ON `stocklist` FOR EACH ROW INSERT
INTO
  `basedata`(`证券代码`,
  `证券简称`)
VALUES(NEW.`证券代码`, NEW.`证券简称`)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `tmp`
--

CREATE TABLE `tmp` (
  `code` varchar(63) NOT NULL,
  `date` date NOT NULL,
  `percentage` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 触发器 `tmp`
--
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
-- 表的结构 `unusual`
--

CREATE TABLE `unusual` (
  `datetime` datetime NOT NULL,
  `code` char(6) NOT NULL,
  `type` enum('60日新低','60日新高','低开5日','向上缺口','向下缺口','大幅上涨','大幅下跌','大笔买入','大笔卖出','封涨停板','封跌停板','快速下跌','快速反弹','打开涨停','打开跌停','有大买盘','有大卖盘','火箭发射','竞价上涨','竞价下跌','高台跳水','高开5日') NOT NULL,
  `data` varchar(63) DEFAULT NULL,
  `goodorbad` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (year(datetime))
(
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION P19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `usefuldata`
--

CREATE TABLE `usefuldata` (
  `code` varchar(30) NOT NULL,
  `date` date NOT NULL DEFAULT '1990-01-01',
  `amorank` int(11) DEFAULT NULL,
  `araise` int(11) DEFAULT NULL,
  `percentage` float DEFAULT NULL,
  `focus` varchar(256) NOT NULL DEFAULT '',
  `taresult` enum('0','1','1,2','2','3','1,3','2,3','1,2,3') DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (YEAR(`date`))
(
PARTITION p92 VALUES LESS THAN (1993)ENGINE=InnoDB,
PARTITION p93 VALUES LESS THAN (1994)ENGINE=InnoDB,
PARTITION p94 VALUES LESS THAN (1995)ENGINE=InnoDB,
PARTITION p95 VALUES LESS THAN (1996)ENGINE=InnoDB,
PARTITION p96 VALUES LESS THAN (1997)ENGINE=InnoDB,
PARTITION p97 VALUES LESS THAN (1998)ENGINE=InnoDB,
PARTITION p98 VALUES LESS THAN (1999)ENGINE=InnoDB,
PARTITION p99 VALUES LESS THAN (2000)ENGINE=InnoDB,
PARTITION p00 VALUES LESS THAN (2001)ENGINE=InnoDB,
PARTITION p01 VALUES LESS THAN (2002)ENGINE=InnoDB,
PARTITION p02 VALUES LESS THAN (2003)ENGINE=InnoDB,
PARTITION p03 VALUES LESS THAN (2004)ENGINE=InnoDB,
PARTITION p04 VALUES LESS THAN (2005)ENGINE=InnoDB,
PARTITION p05 VALUES LESS THAN (2006)ENGINE=InnoDB,
PARTITION p06 VALUES LESS THAN (2007)ENGINE=InnoDB,
PARTITION p07 VALUES LESS THAN (2008)ENGINE=InnoDB,
PARTITION p08 VALUES LESS THAN (2009)ENGINE=InnoDB,
PARTITION p09 VALUES LESS THAN (2010)ENGINE=InnoDB,
PARTITION p10 VALUES LESS THAN (2011)ENGINE=InnoDB,
PARTITION p11 VALUES LESS THAN (2012)ENGINE=InnoDB,
PARTITION p12 VALUES LESS THAN (2013)ENGINE=InnoDB,
PARTITION p13 VALUES LESS THAN (2014)ENGINE=InnoDB,
PARTITION p14 VALUES LESS THAN (2015)ENGINE=InnoDB,
PARTITION p15 VALUES LESS THAN (2016)ENGINE=InnoDB,
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION p19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_login_id` varchar(32) NOT NULL,
  `user_password` varchar(512) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `user_email` text NOT NULL,
  `user_mobile` varchar(11) NOT NULL,
  `user_group` enum('admin','vip','high-end','paid','free') NOT NULL DEFAULT 'free',
  `user_expiration_date` date DEFAULT '2050-12-31'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `user_invitation`
--

CREATE TABLE `user_invitation` (
  `id` int(11) NOT NULL,
  `code` varchar(16) NOT NULL,
  `user_check` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `zdt`
--

CREATE TABLE `zdt` (
  `code` varchar(63) NOT NULL,
  `name` varchar(63) DEFAULT NULL,
  `close` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `fcb` double DEFAULT NULL,
  `flb` double DEFAULT NULL,
  `fdmoney` double DEFAULT NULL,
  `lasttime` datetime DEFAULT NULL,
  `firsttime` datetime NOT NULL,
  `opentimes` bigint(20) DEFAULT NULL,
  `amplitude` double DEFAULT NULL,
  `force` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (year(`firsttime`))
(
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION P19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

-- --------------------------------------------------------

--
-- 表的结构 `zrzdt`
--

CREATE TABLE `zrzdt` (
  `code` varchar(63) NOT NULL,
  `name` varchar(63) DEFAULT NULL,
  `time` datetime NOT NULL,
  `close` double DEFAULT NULL,
  `percentage` double DEFAULT NULL,
  `amo` double DEFAULT NULL,
  `amplitude` double DEFAULT NULL,
  `turnoverate` double DEFAULT NULL,
  `pe` double DEFAULT NULL,
  `concept` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (year(`time`))
(
PARTITION p16 VALUES LESS THAN (2017)ENGINE=InnoDB,
PARTITION p17 VALUES LESS THAN (2018)ENGINE=InnoDB,
PARTITION p18 VALUES LESS THAN (2019)ENGINE=InnoDB,
PARTITION P19 VALUES LESS THAN (2020)ENGINE=InnoDB,
PARTITION p20 VALUES LESS THAN (2021)ENGINE=InnoDB,
PARTITION p21 VALUES LESS THAN (2022)ENGINE=InnoDB,
PARTITION p22 VALUES LESS THAN (2023)ENGINE=InnoDB,
PARTITION p23 VALUES LESS THAN (2024)ENGINE=InnoDB,
PARTITION p24 VALUES LESS THAN (2025)ENGINE=InnoDB,
PARTITION p25 VALUES LESS THAN (2026)ENGINE=InnoDB
);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `5min`
--
ALTER TABLE `5min`
  ADD PRIMARY KEY (`code`,`datetime`);

--
-- Indexes for table `basedata`
--
ALTER TABLE `basedata`
  ADD PRIMARY KEY (`证券代码`),
  ADD KEY `证券简称` (`证券简称`);

--
-- Indexes for table `blocktrade`
--
ALTER TABLE `blocktrade`
  ADD PRIMARY KEY (`id`,`code`,`交易日期`),
  ADD KEY `cdoe` (`code`,`买方营业部`,`卖方营业部`),
  ADD KEY `类型` (`类型`);

--
-- Indexes for table `blog`
--
ALTER TABLE `blog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `buyback`
--
ALTER TABLE `buyback`
  ADD PRIMARY KEY (`证劵代码`,`方案进度`,`董事会通过日`,`股份种类`);

--
-- Indexes for table `capitalchange`
--
ALTER TABLE `capitalchange`
  ADD PRIMARY KEY (`﻿股票代码`,`变动日期`),
  ADD KEY `变动日期` (`变动日期`);

--
-- Indexes for table `cirholder`
--
ALTER TABLE `cirholder`
  ADD PRIMARY KEY (`code`,`date`,`name`);

--
-- Indexes for table `dayline`
--
ALTER TABLE `dayline`
  ADD PRIMARY KEY (`code`,`date`),
  ADD KEY `date` (`date`),
  ADD KEY `code` (`code`);

--
-- Indexes for table `dayline_tmp`
--
ALTER TABLE `dayline_tmp`
  ADD PRIMARY KEY (`code`,`date`),
  ADD KEY `date` (`date`);

--
-- Indexes for table `favorite`
--
ALTER TABLE `favorite`
  ADD PRIMARY KEY (`favorite_id`);

--
-- Indexes for table `financial`
--
ALTER TABLE `financial`
  ADD PRIMARY KEY (`报表日期`,`代码`),
  ADD KEY `代码` (`代码`);

--
-- Indexes for table `financial_rank`
--
ALTER TABLE `financial_rank`
  ADD PRIMARY KEY (`代码`,`报表日期`);

--
-- Indexes for table `forecast`
--
ALTER TABLE `forecast`
  ADD PRIMARY KEY (`code`,`date`,`财报日期`),
  ADD KEY `下限` (`下限`),
  ADD KEY `上限` (`上限`),
  ADD KEY `预告类型` (`预告类型`);

--
-- Indexes for table `ftsplit`
--
ALTER TABLE `ftsplit`
  ADD PRIMARY KEY (`code`,`date`),
  ADD KEY `date` (`date`);

--
-- Indexes for table `incentive`
--
ALTER TABLE `incentive`
  ADD PRIMARY KEY (`股票代码`,`激励标的物`,`薪酬委员会预案公告日`),
  ADD KEY `本期计划制定年度` (`本期计划制定年度`),
  ADD KEY `方案进度` (`方案进度`);

--
-- Indexes for table `indexdb`
--
ALTER TABLE `indexdb`
  ADD PRIMARY KEY (`code`,`date`),
  ADD KEY `date` (`date`);

--
-- Indexes for table `indexlist`
--
ALTER TABLE `indexlist`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `indicator`
--
ALTER TABLE `indicator`
  ADD UNIQUE KEY `short` (`short`);

--
-- Indexes for table `institutional`
--
ALTER TABLE `institutional`
  ADD PRIMARY KEY (`code`,`fundcode`,`date`);

--
-- Indexes for table `lhb`
--
ALTER TABLE `lhb`
  ADD PRIMARY KEY (`index`,`date`,`code`,`上榜原因`),
  ADD KEY `营业部名称` (`营业部名称`);

--
-- Indexes for table `lhb_base`
--
ALTER TABLE `lhb_base`
  ADD PRIMARY KEY (`营业部代码`);

--
-- Indexes for table `mainbusiness`
--
ALTER TABLE `mainbusiness`
  ADD PRIMARY KEY (`code`,`报表日期`,`主营构成`,`分类`);

--
-- Indexes for table `managerial`
--
ALTER TABLE `managerial`
  ADD PRIMARY KEY (`code`,`日期`,`变动人`,`持股种类`,`变动股数`,`变动后持股数`,`成交均价`,`变动人与董监高的关系`,`变动方式`,`变动金额`,`职务`,`变动比例`,`董监高人员姓名`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `link` (`link`),
  ADD KEY `type` (`type`),
  ADD KEY `datetime` (`datetime`);

--
-- Indexes for table `notice`
--
ALTER TABLE `notice`
  ADD PRIMARY KEY (`date`,`infocode`),
  ADD KEY `type` (`type`),
  ADD KEY `eutime` (`eutime`);

--
-- Indexes for table `realtimecal`
--
ALTER TABLE `realtimecal`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `datetime` (`datetime`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `shareholder`
--
ALTER TABLE `shareholder`
  ADD PRIMARY KEY (`code`,`date`,`name`);

--
-- Indexes for table `shareholdernumber`
--
ALTER TABLE `shareholdernumber`
  ADD PRIMARY KEY (`code`,`date`);

--
-- Indexes for table `spo_done`
--
ALTER TABLE `spo_done`
  ADD PRIMARY KEY (`code`,`name`,`发行总数`,`发行日期`);

--
-- Indexes for table `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`date`);

--
-- Indexes for table `stocklist`
--
ALTER TABLE `stocklist`
  ADD PRIMARY KEY (`证券代码`);

--
-- Indexes for table `tmp`
--
ALTER TABLE `tmp`
  ADD PRIMARY KEY (`code`,`date`);

--
-- Indexes for table `unusual`
--
ALTER TABLE `unusual`
  ADD PRIMARY KEY (`datetime`,`code`,`type`);

--
-- Indexes for table `usefuldata`
--
ALTER TABLE `usefuldata`
  ADD PRIMARY KEY (`code`,`date`),
  ADD KEY `taresult` (`taresult`),
  ADD KEY `precentage` (`percentage`),
  ADD KEY `amorank` (`amorank`,`araise`,`focus`),
  ADD KEY `date` (`date`),
  ADD KEY `code` (`code`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `user_invitation`
--
ALTER TABLE `user_invitation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_check` (`user_check`);

--
-- Indexes for table `zdt`
--
ALTER TABLE `zdt`
  ADD PRIMARY KEY (`code`,`firsttime`);

--
-- Indexes for table `zrzdt`
--
ALTER TABLE `zrzdt`
  ADD PRIMARY KEY (`code`,`time`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `blocktrade`
--
ALTER TABLE `blocktrade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=188154;
--
-- 使用表AUTO_INCREMENT `blog`
--
ALTER TABLE `blog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- 使用表AUTO_INCREMENT `favorite`
--
ALTER TABLE `favorite`
  MODIFY `favorite_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=598;
--
-- 使用表AUTO_INCREMENT `news`
--
ALTER TABLE `news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41999;
--
-- 使用表AUTO_INCREMENT `realtimecal`
--
ALTER TABLE `realtimecal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=614;
--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- 使用表AUTO_INCREMENT `user_invitation`
--
ALTER TABLE `user_invitation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;
--
-- 限制导出的表
--

--
-- 限制表 `basedata`
--
ALTER TABLE `basedata`
  ADD CONSTRAINT `basedata_ibfk_1` FOREIGN KEY (`证券代码`) REFERENCES `stocklist` (`证券代码`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
