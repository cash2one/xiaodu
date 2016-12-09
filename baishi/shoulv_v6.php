<?php
require_once("shoulv_api.php");
class shoulu_v6 extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://v.6.cn/api/getVideoInfo.php?url=";
	public $site ="v.6.cn";
	public $site_name ="六间房";
	public $fileInputUrls ="data/urls_v.6.cn";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
