<?php
require_once("shoulv_api.php");
class shoulu_ctv extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://api.people.cn/baidu/relative?playerurl=";
	public $site ="ctvplayer.people.cn";
	public $site_name ="CTV";
	public $fileInputUrls ="data/urls_ctvplayer.people.cn";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
