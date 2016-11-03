<?php
require_once("shoulv_api.php");
class shoulu_fun extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://api.fun.tv/api/baidu_video/?res=";
	public $site ="fun.tv";
	public $site_name ="风行网";
	public $fileInputUrls ="data/urls_fun.tv";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
