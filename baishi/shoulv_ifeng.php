<?php
require_once("shoulv_api.php");
class shoulu_ifeng extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://dyn.v.ifeng.com/baiduVideo/getVideoInfo?vlink=";
	public $site ="ifeng.com";
	public $site_name ="凤凰网";
	public $fileInputUrls ="data/urls_ifeng.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
