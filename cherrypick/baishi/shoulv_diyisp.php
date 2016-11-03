<?php
require_once("shoulv_api.php");
class shoulu_diyisp extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	//public $apiFormat ="http://ynews.v1.cn/news/rec-news-fbd/?url=";
	//public $apiFormat ="http://api.v1.cn/v1Enhanced/news/cropNewsFbdv2?url=";
	public $apiFormat ="http://pgcapi.v1.cn/index.php/website_api/baidu/index?url=";
	public $site ="v1.cn";
	public $site_name ="第一视频";
	public $fileInputUrls ="data/urls_v1.cn";
	public $hotRelLinkSigns = "08808156236622605692$$08659783241266763121$$08228970881564351745$$08360353772211046478$$08628361475282565896$$08619982170228628562$$08639981268843186453$$08652164776791751287$$08962418830418871040$$08489325751750567382";
	public $needRelLink = true;
	public $sleepInter = 10000;
}

?>
