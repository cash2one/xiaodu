-- MySQL dump 10.13  Distrib 5.5.30, for Linux (x86_64)
--
-- Host: 10.114.32.36    Database: cherrypick_db
-- ------------------------------------------------------
-- Server version	5.5.30-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `crawl_data_test`
--

DROP TABLE IF EXISTS `crawl_data_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crawl_data_test` (
  `page_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '表主键',
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '标题',
  `horizontal_thumnail_url` varchar(512) NOT NULL DEFAULT '' COMMENT '横版缩略图',
  `horizontal_thumnail_sign1` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '提图签名1',
  `horizontal_thumnail_sign2` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '提图签名2',
  `vertical_thumnail_url` varchar(512) NOT NULL DEFAULT '' COMMENT '竖版缩略图',
  `vertical_thumnail_sign1` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '提图签名1',
  `vertical_thumnail_sign2` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '提图签名2',
  `description` varchar(1024) NOT NULL DEFAULT '' COMMENT '简介',
  `author` varchar(64) NOT NULL DEFAULT '' COMMENT '作者',
  `link` varchar(255) NOT NULL DEFAULT '' COMMENT '播放链接',
  `link_sign1` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '播放链接签名1',
  `link_sign2` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '播放链接签名2',
  `block` varchar(32) NOT NULL DEFAULT '' COMMENT '区块名称（首页或者某个频道）',
  `play_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '播放次数',
  `comment_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '评论次数',
  `up_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞|顶次数',
  `down_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '踩次数',
  `pub_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '发布时间',
  `insert_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '插入时间',
  `update_time` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '更新时间',
  `site` varchar(64) NOT NULL DEFAULT '' COMMENT 'app名称|site名称',
  `state` tinyint(4) NOT NULL DEFAULT '0' COMMENT '入库数据状态：0-新入库，1-已生效，2-下线',
  `flag_dead` tinyint(4) NOT NULL DEFAULT '0' COMMENT '死链状态：0-活链，非0-死链',
  `horizontal_thumnail_score` tinyint(4) NOT NULL DEFAULT '100' COMMENT '缩略图质量评分：0-100',
  `vertical_thumnail_qlevel` tinyint(4) NOT NULL DEFAULT '100' COMMENT '缩略图质量评分：0-100',
  `definition_qlevel` tinyint(4) NOT NULL DEFAULT '1' COMMENT '视频内容清晰度质量等级：1-清晰，2-中，3-模糊',
  `title_qlevel` tinyint(4) NOT NULL DEFAULT '1' COMMENT '标题文本质量等级：1-好，2-中，3-差',
  `duration` int(10) NOT NULL DEFAULT '0',
  `real_link` varchar(256) NOT NULL DEFAULT '',
  `hd` int(10) NOT NULL DEFAULT '0',
  `bos_link` varchar(2048) NOT NULL DEFAULT '',
  PRIMARY KEY (`page_id`),
  UNIQUE KEY `link_index` (`link`),
  KEY `site_idx` (`site`)
) ENGINE=InnoDB AUTO_INCREMENT=227969 DEFAULT CHARSET=utf8 COMMENT='优质数据原始数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crawl_data_test`
--
-- WHERE:  1=1 order by insert_time desc limit 10

LOCK TABLES `crawl_data_test` WRITE;
/*!40000 ALTER TABLE `crawl_data_test` DISABLE KEYS */;
INSERT INTO `crawl_data_test` VALUES (227959,'【守望逗比】第十五期 我是死亡天使','http://i2.hdslb.com/bfs/archive/3cf2a1fcd2f4a857410ffdfd0b583b8f81e0f4c4.jpg',0,0,'',0,0,'','守望逗比','http://www.bilibili.com/mobile/video/av6821361.html',1737425901,2673525312,'游戏',0,0,0,0,1477381337,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227960,'英雄联盟动画 蛮族之王 - 泰达米尔 强壮的右手 lol英雄联盟','http://i0.hdslb.com/bfs/archive/2ca3236c2da726128865f225c0e415eccf88c40f.jpg_320x200.jpg',0,0,'',0,0,'','M.Scarlet','http://www.bilibili.com/mobile/video/av6820385.html',1813194019,2733568974,'游戏',1556,0,0,0,1477381339,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227961,'糖醋藕丁-迷迭香','http://i1.hdslb.com/bfs/archive/b02ef49df9d544339d810518729bf12b46ce8d40.jpg_320x200.jpg',0,0,'',0,0,'','迷迭香Rosemary美食','http://www.bilibili.com/mobile/video/av5380803.html',1660527125,2751492100,'生活',1449,11,0,0,1477381340,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227962,'【屎蛋说18】预告片和预搞骗','http://i2.hdslb.com/bfs/archive/282bbfe39771d67c0bb2256eadf68fda2db355a3.jpg_320x200.jpg',0,0,'',0,0,'','史丹利快爆','http://www.bilibili.com/mobile/video/av4095870.html',1753458902,2731980198,'游戏',281999,640,0,0,1477381337,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227963,'【Boxbox】锐雯 vs 剑姬 10月11日','http://i1.hdslb.com/bfs/archive/a675cd8f84fabfe31f592ff5e20a157e602cae3c.jpg',0,0,'',0,0,'','SaberZC','http://www.bilibili.com/mobile/video/av6821441.html',1716713992,2678084335,'游戏',0,0,0,0,1477381338,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227964,'划水划水(°∀°)ﾉ','http://i2.hdslb.com/bfs/archive/f7ad5ba2613d1239bbc5b89613663c6b1dd7a3ba.jpg',0,0,'',0,0,'','紫荆酱ちゃん','http://www.bilibili.com/mobile/video/av6821355.html',1786628026,2725589087,'游戏',0,0,0,0,1477381339,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227965,'[BO3]COD12日常瞬狙练习，最后trickshot成功~','http://i0.hdslb.com/bfs/archive/69fe29088710fab92fea22d815e83153579ced43.png_320x200.png',0,0,'',0,0,'','拉神Prophet','http://www.bilibili.com/mobile/video/av6214968.html',1858134190,2781596736,'游戏',193,0,0,0,1477381337,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227966,'【Love live】『CACC』我们是合而为一的光芒 仆光 ☆呼啾呼啾童萌会★','http://i0.hdslb.com/bfs/archive/a0b03a0f9f24164ceb4aba5b10cc4c6e01c03ea7.jpg_320x200.jpg',0,0,'',0,0,'','靳元方丶','http://www.bilibili.com/mobile/video/av4540401.html',1599876091,2642626288,'舞蹈',43753,547,0,0,1477381338,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227967,'【艾尔之光】守护者HA','http://i0.hdslb.com/bfs/archive/33fe0abe3bb7b2488923b4da76c0f9130573f25d.jpg',0,0,'',0,0,'','uml09804','http://www.bilibili.com/mobile/video/av6821357.html',1818403542,2753581621,'游戏',0,0,0,0,1477381338,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,''),(227968,'【BuzzFeed】3美元的寿司和250美元的寿司有什么区别？我看饿了【暂未成立字幕组 中英字幕】','http://i2.hdslb.com/bfs/archive/483e320b7d6d12c23826f4484605bf7146b45dfc.jpg_320x200.jpg',0,0,'',0,0,'','LaoxieH','http://www.bilibili.com/mobile/video/av6391235.html',1714191205,2736866408,'生活',68175,0,0,0,1477381340,1477381342,0,'bilibili',0,0,100,100,1,1,0,'',0,'');
/*!40000 ALTER TABLE `crawl_data_test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-28 11:40:31
