<?php
require_once("shoulv_api.php");
class shoulu_yy extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://www.yy.com/u/video/forbaidu?playUrl=";
	public $site ="yy.com";
	public $site_name ="yy视频";
	public $fileInputUrls ="data/urls_yy.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
