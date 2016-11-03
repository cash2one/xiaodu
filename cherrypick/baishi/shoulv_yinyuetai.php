<?php
require_once("shoulv_api.php");
class shoulu_yinyuetai extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://api.yinyuetai.com/api/baidu/short-video-data?currentPage=";
	public $site ="yinyuetai.com";
	public $site_name ="音乐台";
	public $fileInputUrls ="data/urls_yinyuetai.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
