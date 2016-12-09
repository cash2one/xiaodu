<?php
require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

class shoulu_api {

	public $mapCategory3To2 = array(
		"公共英语"=>"英语培训",
		"英语口语"=>"英语培训",
		"商务英语"=>"英语培训",
		"托福"=>"英语培训",
		"雅思"=>"英语培训",
		"CET"=>"英语培训",
		"GRE"=>"英语培训",
		"GMAT"=>"英语培训",
		"SAT"=>"英语培训",
		"SSAT"=>"英语培训",
		"KET"=>"英语培训",
		"新概念英语"=>"英语培训",
		"少儿英语"=>"英语培训",
		"职称英语"=>"英语培训",
		"成人英语"=>"英语培训",
		"alevel"=>"英语培训",
		"其他"=>"英语培训",
		"日语"=>"小语种",
		"韩语"=>"小语种",
		"其他"=>"小语种",
		"职称证书"=>"IT培训",
		"电脑基础"=>"IT培训",
		"设计制作"=>"IT培训",
		"编程开发"=>"IT培训",
		"数据库管理"=>"IT培训",
		"公务员"=>"资格认证",
		"建筑工程"=>"资格认证",
		"金融会计"=>"资格认证",
		"医药培训"=>"资格认证",
		"贸易外贸"=>"资格认证",
		"企业管理"=>"资格认证",
		"健康保健"=>"资格认证",
		"职业资格"=>"资格认证",
		"管理通用"=>"管理培训",
		"企业运营"=>"管理培训",
		"设计制作"=>"技能培训",
		"媒体艺术"=>"技能培训",
		"工程维修"=>"技能培训",
		"实用技能"=>"技能培训",
		"创业求职"=>"技能培训",
		"考研辅导"=>"考研",
		"法律研究生"=>"考研",
		"工程研究生"=>"考研",
		"教育研究生"=>"考研",
		"心理学研究生"=>"考研",
		"艺术研究所"=>"考研",
		"其他"=>"考研",
		"欧洲留学"=>"留学",
		"美洲留学"=>"留学",
		"澳洲留学"=>"留学",
		"亚洲留学"=>"留学",
		"其他"=>"留学",
		"高一"=>"高中",
		"高二"=>"高中",
		"高三"=>"高中",
		"高考"=>"高中",
		"素质教育"=>"高中",
		"其他"=>"高中",
		"初一"=>"初中",
		"初二"=>"初中",
		"初三"=>"初中",
		"中考"=>"初中",
		"素质教育"=>"初中",
		"其他"=>"初中",
		"学前班"=>"小学",
		"一年级"=>"小学",
		"二年级"=>"小学",
		"三年级"=>"小学",
		"四年级"=>"小学",
		"五年级"=>"小学",
		"六年级"=>"小学",
		"小升初"=>"小学",
		"素质教育"=>"小学",
		"其他"=>"小学",
		"声乐培训"=>"文体艺术",
		"美术培训"=>"文体艺术",
		"健身培训"=>"文体艺术",
		"影视艺术"=>"文体艺术",
		"其他"=>"文体艺术",
		"演讲与口才"=>"兴趣",
		"特殊技能"=>"兴趣",
		"驾驶"=>"兴趣",
		"美食"=>"兴趣",
		"养生"=>"兴趣",
		"美容"=>"兴趣",
		"风水"=>"兴趣",
		"励志"=>"兴趣",
		"孕妇培训"=>"生活技能",
		"生存逃生"=>"生活技能",
		"其他"=>"生活技能",

		"公开课"=>"公开课",
		"生活理财"=>"生活理财",
	);
	public $mapCategory3To1 = array(
		"公共英语"=>"外语",
		"英语口语"=>"外语",
		"商务英语"=>"外语",
		"托福"=>"外语",
		"雅思"=>"外语",
		"CET"=>"外语",
		"GRE"=>"外语",
		"GMAT"=>"外语",
		"SAT"=>"外语",
		"SSAT"=>"外语",
		"KET"=>"外语",
		"新概念英语"=>"外语",
		"少儿英语"=>"外语",
		"职称英语"=>"外语",
		"成人英语"=>"外语",
		"alevel"=>"外语",
		"其他"=>"外语",
		"日语"=>"外语",
		"韩语"=>"外语",
		"其他"=>"外语",
		"职称证书"=>"职业培训",
		"电脑基础"=>"职业培训",
		"设计制作"=>"职业培训",
		"编程开发"=>"职业培训",
		"数据库管理"=>"职业培训",
		"公务员"=>"职业培训",
		"建筑工程"=>"职业培训",
		"金融会计"=>"职业培训",
		"医药培训"=>"职业培训",
		"贸易外贸"=>"职业培训",
		"企业管理"=>"职业培训",
		"健康保健"=>"职业培训",
		"职业资格"=>"职业培训",
		"管理通用"=>"职业培训",
		"企业运营"=>"职业培训",
		"设计制作"=>"职业培训",
		"媒体艺术"=>"职业培训",
		"工程维修"=>"职业培训",
		"实用技能"=>"职业培训",
		"创业求职"=>"职业培训",
		"考研辅导"=>"学历教育",
		"法律研究生"=>"学历教育",
		"工程研究生"=>"学历教育",
		"教育研究生"=>"学历教育",
		"心理学研究生"=>"学历教育",
		"艺术研究所"=>"学历教育",
		"其他"=>"学历教育",
		"欧洲留学"=>"学历教育",
		"美洲留学"=>"学历教育",
		"澳洲留学"=>"学历教育",
		"亚洲留学"=>"学历教育",
		"其他"=>"学历教育",
		"高一"=>"中小学",
		"高二"=>"中小学",
		"高三"=>"中小学",
		"高考"=>"中小学",
		"素质教育"=>"中小学",
		"其他"=>"中小学",
		"初一"=>"中小学",
		"初二"=>"中小学",
		"初三"=>"中小学",
		"中考"=>"中小学",
		"素质教育"=>"中小学",
		"其他"=>"中小学",
		"学前班"=>"中小学",
		"一年级"=>"中小学",
		"二年级"=>"中小学",
		"三年级"=>"中小学",
		"四年级"=>"中小学",
		"五年级"=>"中小学",
		"六年级"=>"中小学",
		"小升初"=>"中小学",
		"素质教育"=>"中小学",
		"其他"=>"中小学",
		"声乐培训"=>"实用教程",
		"美术培训"=>"实用教程",
		"健身培训"=>"实用教程",
		"影视艺术"=>"实用教程",
		"其他"=>"实用教程",
		"演讲与口才"=>"实用教程",
		"特殊技能"=>"实用教程",
		"驾驶"=>"实用教程",
		"美食"=>"实用教程",
		"养生"=>"实用教程",
		"美容"=>"实用教程",
		"风水"=>"实用教程",
		"励志"=>"实用教程",
		"孕妇培训"=>"实用教程",
		"生存逃生"=>"实用教程",
		"其他"=>"实用教程",

		"公开课"=>"公开课",
		"生活理财"=>"生活理财",
	);

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	//init the relLinks when having no realtedStreams
	public $hotRelLinkSigns = "";
	
	public $originDB;
	public $context;
	public $header;
	public $isDebug = false;

	public $cLevel1 = 1;
	public $cLevel2 = 2;
	public $cLevel3 = 3;
	//get category2 by category3
	public $cLevel32 = 32;
	//get category1 by category3
	public $cLevel31 = 31;

	public $apiFormat="";
	public $site="";
	public $site_name="";
	public $fileInputUrls="";
	public $needRelLink=false;
	public $relItems ="relatedStreams";
	public $needUrlEncode = false;
	public $needUrlDecode = false;
	public $needSaveTagUrlRel = true;
	public $needSaveCategoryAstag = true;
	public $needFetchFromNet = false;
	public $mustHaveRelLink = true;
	public $fileType = 1;
	//url is both in urlfile and in json return value. but play_link of jiaoyu.baidu.com is in json return value.
	public $useInnerUrl = false;
	public $sleepInter = 500000;

	function init(){
		//mysql connect
		$this->originDB=new SendMysql();
		$status = $this->originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
		if ($status != ErrorNo::$RET_SUCCESS ){
			exit("failed to connect to mysql");
		}
		$opts = array(
			'http'=>array(
				'method'=>"GET",
				'header'=> "Cookie: app-id=101",
				'timeout'=> 10,
			)
		);
		$this->context = stream_context_create($opts);

		$this->header = array(
			'method: GET',
			'api-id: 101'
		);
	}

	//分类映射
	function categoryMap($category, $level){
		$mappingCategory ="";
		switch($level){
		case $this->cLevel1:
			if(array_key_exists($category, $this->mapCategoryLevel1)) $mappingCategory = $this->mapCategoryLevel1["$category"];
			break;
		case $this->cLevel2:
			if(array_key_exists($category, $this->mapCategoryLevel2)) $mappingCategory = $this->mapCategoryLevel2["$category"];
			break;
		case $this->cLevel3:
			if(array_key_exists($category, $this->mapCategoryLevel3)) $mappingCategory = $this->mapCategoryLevel3["$category"];
			break;
		case $this->cLevel31:
			if(array_key_exists($category, $this->mapCategory3To1)) $mappingCategory = $this->mapCategory3To1["$category"];
			break;
		case $this->cLevel32:
			if(array_key_exists($category, $this->mapCategory3To2)) $mappingCategory = $this->mapCategory3To2["$category"];
			break;
		default:
			echo"categroy level invalid:[$level]\n";
		}
		//echo"+++++++++++map-input[$category], out[$mappingCategory] level[$level]\n";
		return $mappingCategory;
	}
	
	function categoryOfBaishiMap($category1, $category2, $category3){
		//category map and save
		$category1 = self::categoryMap($category1, $this->cLevel1);
		$category2 = self::categoryMap($category2, $this->cLevel2);
		$category3 = self::categoryMap($category3, $this->cLevel3);
		if($this->isDebug) echo "first mapping result: c-1[$category1] c-2[$category2] c-3[$category3] \n";
		if(strlen($category1) < 1 && strlen($category3) > 1)
			$category1 = self::categoryMap($category3, $this->cLevel31);
		if(strlen($category2) < 1 && strlen($category3) > 1)
			$category2 = self::categoryMap($category3, $this->cLevel32);
		if($this->isDebug) echo "second mapping result: c-1[$category1] c-2[$category2] c-3[$category3] \n";
		$categoryBs = "";
		if(strlen($category1) > 0){
			$categoryBs = $category1;
			if(strlen($category2) > 0){
				$categoryBs = $category1."=>".$category2;
				if(strlen($category3) > 0){
					$categoryBs = $category1."=>".$category2."=>".$category3;
				}
			}
		}
		//echo"++++++++++map-[$categoryBs] [$category1, $category2, $category3]\n";
		return $categoryBs;
	}

	function saveTagUrlRel($tags, $sign64){
		$tmpstr = str_replace("=>","$$", $tags);
		$parts = explode("$$", $tmpstr);
		foreach($parts as $part){
			if(strlen($part) < 1) continue;
			$cmtTag ="insert into tbl_tag_urlsign set tag='".$part."', play_link_sign64='".$sign64."' ;";
			if($this->isDebug) echo "cmt-aveTagUrlRel $cmtTag\n";
			$this->originDB->oprationDB($cmtTag);
		}
	}

	function saveCategoryAsTag($category, $sign64){
		if(strlen($category)>4){
			$cmtTag ="insert into tbl_tag_urlsign set tag='".$category."', play_link_sign64='".$sign64."' ;";
			if($this->isDebug) echo "cmt-saveCategoryAsTag: $cmtTag\n";
			$this->originDB->oprationDB($cmtTag);
		}
	}
	
	function getUrlInfoDb($url){
		$retVal = array();
		//parameter check
		if(strlen($url) < 7){
			$retVal["status"] = 11;
			$retVal["msg"] = "bad url[$url]";
			return json_encode($retVal);
		}
		$url = trim($url);
		if(! $this->originDB){
			if($this->isDebug) echo"init mysql connection";
			self::init();
		}
		$sign = creat_sign_fs64($url);
		$sign64 = str_replace("-","0",$sign[2]);
		$tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
		if($this->isDebug) echo"main: url[$url] sign64[$sign64] sign1[".$sign[0]."] sign2[".$sign[1]."]\n";
		//get info from db
		$cmtSel ="select * from tbl_video_$tblNumMain where link_sign1=".$sign[0]." and link_sign2=".$sign[1]." and site = '$this->site' ;";
		if($this->mustHaveRelLink){
			$cmtSel ="select * from tbl_video_$tblNumMain where link_sign1=".$sign[0]." and link_sign2=".$sign[1]." and site = '$this->site' and rel_link_sign64s != '' and rel_link_sign64s != '$this->hotRelLinkSigns';";
		}
		$items = $this->originDB->oprationDB($cmtSel);
		$len = mysql_num_rows($items);
		if($this->isDebug) echo"cmt: $cmtSel len[$len]\n";
		if($len > 1){
			$retVal["status"] = 10;
			$retVal["msg"] ="get info from DB failed! cmt[$cmtSel] len[]";
			return json_encode($retVal);
		}
		if($len < 1){
			if($this->isDebug) echo"get info from api url[$url]\n";
			$retVal["status"] = 10;
			$retVal["msg"] =" url not in DB! and api of baidujiaoyu is not valid NOW ";
			//return json_encode($retVal);
			return self::processUrl($url);
		}
		if($this->isDebug) echo"get info from db\n";
		$mitem = mysql_fetch_assoc($items) or exit("fetch failed!");
		if($mitem->flag_dead != 0){
			$retVal["status"] = 10;
			$retVal["msg"] = "url is dead!";
		}else{
			$retVal["status"] = 0;
			$retVal["msg"] = "";
		}
		$retVal["url"] ="http://baishi.baidu.com/watch/$sign64.html";
		return json_encode($retVal);
	}

	function processUrl($url){
		//返回值
		$retVal = array();
		$url = trim($url);
		if(! $this->originDB){
			if($this->isDebug) echo"init mysql connection";
			self::init();
		}
		if($this->needUrlDecode){
			$url = urldecode($url);
		}
		$sign = creat_sign_fs64($url);
		$sign64 = str_replace("-","0",$sign[2]);
		if($this->isDebug) echo"main: url[$url] sign64[$sign64]\n";
		$tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
		if($this->needUrlEncode){
			$urlEncode = urlencode($url);
			$url = $this->apiFormat.$urlEncode;
		}else{
			$url = $this->apiFormat.$url;
		}
		if($this->isDebug) echo "get apiurl[$url]\n";
		$rawdata = file_get_contents($url,false,$this->context);
		if(false == $rawdata){
			if($this->isDebug) echo"file_get_contents: $url \n";
			$retVal["status"] = 1;
			$retVal["msg"] ="get info from api failed!";
			return json_encode($retVal);
		}
		$mitem = json_decode(htmlspecialchars_decode($rawdata));
		list($duH,$duM,$duS) = split(":",$mitem->duration,3);
		if($this->isDebug) echo "duH:$duH duM:$duM duS:$duS";
		if($duH > 0 && $duM == 0 && $duS == 0){
			$duration = $mitem->duration;
		}else if($duS == ""){
			$duration = $duH * 60 + $duM;
		}else{
			$duration = $duH * 3600 + $duM * 60 + $duS;
		}
		if($duration < 1 && strlen($mitem->imghUrl) < 7 && strlen($mitem->swf) < 7){
			if($this->isDebug) echo"url maybe dead:$url \n";
			$retVal["status"] = 2;
			$retVal["msg"] ="url has no duration and no swf. duration[$duration] imghUrl[".$mitem->imghUrl."] swf[".$mitem->swf."]";
			return json_encode($retVal);
		}
		if($this->useInnerUrl){
			$innerUrl = $mitem->url;
			$sign = creat_sign_fs64($innerUrl);
			$sign64 = str_replace("-","0",$sign[2]);
			$tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
			if($this->isDebug) echo"use inner url: url[$innerUrl] sign64[$sign64] tblNumMain[$tblNumMain]\n";
		}
		
		//category map and save
		$category_ori = $mitem->category1."=>".$mitem->category2."=>".$mitem->category3;
		$category = self::categoryOfBaishiMap($mitem->category1, $mitem->category2, $mitem->category3);
		if($this->isDebug) echo"categoryOfBaishiMap. categorys[$category] \n";
		if($this->needSaveCategoryAstag){
			self::saveCategoryAsTag($category, $sign64);
			self::saveCategoryAsTag($category_ori, $sign64);
		}
		//save tag-url
		$tags = $category."$$".$mitem->tags."$$".$mitem->category1."$$".$mitem->category2."$$".$mitem->category3;
		if($this->isDebug) echo"saveTagUrlRel. tags[$tags] \n";
		if($this->needSaveTagUrlRel){
			self::saveTagUrlRel($tags, $sign64);
		}

		$imgurl = $mitem->imghUrl;
		$this->site = $mitem->site;
		//接口标准兼容
		$tag_mitem = $mitem->tags;
		if($tag_mitem == ""){
			$tag_mitem = $mitem->tag;
		}
		$cmtMain ="insert into tbl_video_$tblNumMain set categorys='$category', tags='$tag_mitem', album_name='$mitem->album', album_index='$mitem->albumIndex', title='$mitem->title', play_link='$mitem->url', real_link='$mitem->swf', file_type=1, image_link='$imgurl', duration=$duration, time_publish='$mitem->updateTime' , site = '$this->site', site_name = '$this->site_name', link_sign1=".$sign[0].", link_sign2=".$sign[1].", play_link_sign64='".$sign64."', time_opt=now(), rel_link_sign64s='$this->hotRelLinkSigns', categorys_ori='$category_ori' ;";
		$cmtMainUpdate ="update tbl_video_$tblNumMain set categorys='$category', tags='$tag_mitem', album_name='$mitem->album', album_index='$mitem->albumIndex', title='$mitem->title', play_link='$mitem->url', real_link='$mitem->swf', file_type=1, image_link='$imgurl', duration=$duration, time_publish='$mitem->updateTime' , site = '$this->site', site_name = '$this->site_name', play_link_sign64='".$sign64."', time_opt=now(), categorys_ori='$category_ori' where link_sign1=".$sign[0]." and link_sign2=".$sign[1]."  ;";
		if($this->isDebug) echo"cmt: $cmtMain\n";
		$statusMain = $this->originDB->oprationDB($cmtMain);
		if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
			if($this->isDebug) echo"insert failed. go to update \n";
			if($this->isDebug) echo"update-cmt: $cmtMainUpdate\n";
			$statusMain = $this->originDB->oprationDB($cmtMainUpdate);
			if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
				if($this->isDebug) echo"update-cmt failed: $cmtMainUpdate \n";
				$retVal["status"] = 3;
				$retVal["msg"] ="failed to save url! cmt[$cmtMainUpdate]";
				return json_encode($retVal);
			}
		}
		//save album
		if(strlen($mitem->album)>2){
			$albumLink ="".$mitem->albumLink.$mitem->album;
			$cmtSaveAlbum ="replace into tbl_album_urlsign set site='$this->site', album_name='$mitem->album',album_link='".$albumLink."', album_index='$mitem->albumIndex', play_link_sign64='".$sign64."';";
			if($this->isDebug) echo "cmt-tbl_album_urlsign: $cmtSaveAlbum\n";
			$statusAlbum = $this->originDB->oprationDB($cmtSaveAlbum);
			if($statusAlbum === ErrorNo::$RET_MYSQL_ERROR){
				if($this->isDebug) echo"album-cmt failed: $cmtSaveAlbum \n";
				$retVal["status"] = 3;
				$retVal["msg"] ="failed to save album! cmt[$cmtSaveAlbum]";
				return json_encode($retVal);
			}
		}
		$relSigns="";
		$relItemsTmp = $this->relItems;
		$items = $mitem->$relItemsTmp;
		foreach($items as $item){
			$imgurlRel = $item->imghUrl;
			$urlRel = $item->url;
			$signRel = creat_sign_fs64($item->url);
			$signRel64 = str_replace("-","0",$signRel[2]);
			$tblNumRel = (($signRel[0] + $signRel[1]) % 64) + 1;

			list($duH,$duM,$duS) = split(":",$item->duration,3);
			$duration = 0;
			if($this->isDebug) echo"Rel: url[$urlRel] sign64[$signRel64]\n";
			if($duH > 0 && $duM == 0 && $duS == 0){
				$duration = $mitem->duration;
			}else if($duS == ""){
				$duration = $duH * 60 + $duM;
			}else{
				$duration = $duH * 3600 + $duM * 60 + $duS;
			}

			//category map and save
			$categoryRel_ori = $item->category1."=>".$item->category2."=>".$item->category3;
			$categoryRel = self::categoryOfBaishiMap($item->category1, $item->category2, $item->category3);
			if($this->isDebug) echo"categoryOfBaishiMap-REL. categorys[$categoryRel] \n";
			if($this->needSaveCategoryAstag){
				self::saveCategoryAsTag($categoryRel, $signRel64);
				self::saveCategoryAsTag($categoryRel_ori, $signRel64);
			}
			if(strlen($categoryRel)>4){
				$cmtTag ="insert into tbl_tag_urlsign set tag='".$categoryRel."', play_link_sign64='".$signRel64."' ;";
				$this->originDB->oprationDB($cmtTag);
			}
			//save tag-url
			$tags = $categoryRel."$$".$item->tag."$$".$item->category1."$$".$item->category2."$$".$item->category3;
			if($this->isDebug) echo"saveTagUrlRel-REL. tags[$tags] \n";
			if($this->needSaveTagUrlRel){
				self::saveTagUrlRel($tags, $signRel64);
			}

			//接口标准兼容
			$tag_item = $item->tag;
			if($tag_item == ""){
				$tag_item = $item->tags;
			}


			$album_item = $item->album;
			if($album_item == ""){
				$album_item = $mitem->album;
			}
			$cmtRel ="insert into tbl_video_$tblNumRel set categorys='$categoryRel', tags='$tag_item', album_name='$album_item', album_index='$item->albumIndex', title='$item->title', play_link='$item->url', real_link='$item->swf', file_type=1, image_link='$imgurlRel', duration=$duration, time_publish='$item->updateTime', site='$this->site', site_name = '$this->site_name', link_sign1=".$signRel[0].", link_sign2=".$signRel[1].", play_link_sign64='".$signRel64."', time_opt=now(), rel_link_sign64s='$this->hotRelLinkSigns', categorys_ori='$categoryRel_ori';";
			$cmtRelUpdate ="update tbl_video_$tblNumRel set categorys='$categoryRel', tags='$tag_item', album_name='$album_item', album_index='$item->albumIndex', title='$item->title', play_link='$item->url', real_link='$item->swf', file_type=1, image_link='$imgurlRel', duration=$duration, time_publish='$item->updateTime', site='$this->site', site_name = '$this->site_name', play_link_sign64='".$signRel64."', time_opt=now(), categorys_ori='$categoryRel_ori' where link_sign1=".$signRel[0]." and link_sign2=".$signRel[1].";";
			if($this->isDebug) echo"cmt: $cmtRel \n";
			$status = $this->originDB->oprationDB($cmtRel);
			if($status === ErrorNo::$RET_MYSQL_ERROR){
				if($this->isDebug) echo"insert rel failed. go to update \n";
				if($this->isDebug) echo"update-cmt of rel: $cmtRelUpdate\n";
				$status = $this->originDB->oprationDB($cmtRelUpdate);
				if($status === ErrorNo::$RET_MYSQL_ERROR){
					if($this->isDebug) echo"update-cmt of rel failed!: $cmtRelUpdate\n";
					continue;
				}
			}
			if(strlen($item->album) > 2){
				$albumLink ="".$item->albumLink.$item->album;
				$cmtSaveAlbum ="replace into tbl_album_urlsign set site='$this->site', album_name='$item->album',album_link='".$albumLink."', album_index='$item->albumIndex', play_link_sign64='".$signRel64."';";
				if($this->isDebug) echo "cmt-tbl_album_urlsign: $cmtSaveAlbum\n";
				$statusAlbum = $this->originDB->oprationDB($cmtSaveAlbum);
				if($statusAlbum === ErrorNo::$RET_MYSQL_ERROR){
					if($this->isDebug) echo"album-cmt-rel failed: $cmtSaveAlbum \n";
					$retVal["status"] = 3;
					$retVal["msg"] ="failed to save album-rel! cmt[$cmtSaveAlbum]";
					return json_encode($retVal);
				}
			}
			if(strlen($relSigns) < 1){
				$relSigns = $signRel64;
			}else{
				$relSigns = $relSigns."$$".$signRel64;
			}
		}
		if($this->needRelLink){
			if(strlen($relSigns) < 1){
				$relSigns = $this->hotRelLinkSigns;
			}
			$cmtRelUpd ="update tbl_video_$tblNumMain set rel_link_sign64s='$relSigns' where link_sign1=".$sign[0]." and link_sign2=".$sign[1]." ;";
			if($this->isDebug) echo"cmtRelUpd: $cmtRelUpd \n";
			$this->originDB->oprationDB($cmtRelUpd);
		}
		
		foreach($items as $item){
			$signRel = creat_sign_fs64($item->url);
			$signRel64 = str_replace("-","0",$signRel[2]);
			$tblNumRel = (($signRel[0] + $signRel[1]) % 64) + 1;

			$cmtRelUpd ="update tbl_video_$tblNumRel set rel_link_sign64s='$relSigns' where link_sign1=".$signRel[0]." and link_sign2=".$signRel[1]." ;";
			if($this->isDebug) echo"cmtRelUpd: $cmtRelUpd \n";
			$this->originDB->oprationDB($cmtRelUpd);
		}		

		//return msg of json 
		$retVal["status"] = 0;
		$retVal["msg"] ="";
		$retVal["sign64"] =$sign64;
		$retVal["url"] ="http://baishi.baidu.com/watch/$sign64.html";
		return json_encode($retVal);
	}
	
	function run(){
		$fhandle = fopen($this->fileInputUrls,"r") or exit (" failed to open url file[$this->fileInputUrls]\n");
		$lineCount = 1;
		while(false !== ($line = fgets($fhandle, 256))){
			if($this->isDebug) echo"now process at[$lineCount]\n";
			$lineCount += 1;
			if($this->needFetchFromNet){
				self::processUrl(trim($line));
			}else{
				self::getUrlInfoDb(trim($line));
			}
			usleep($this->sleepInter);
		}
	}
}
?>
