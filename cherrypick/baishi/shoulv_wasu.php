<?php
require_once("shoulv_api.php");
class shoulu_wasu extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://api.wasu.cn/vod/baidu/videoapi?url=";
	public $site ="wasu.cn";
	public $site_name ="华数";
	public $fileInputUrls ="data/urls_wasu.cn";
	public $needRelLink = true;
	public $hotRelLinkSigns = "02446319187893235909$$02348330982210830241$$02338809417684553252$$02414797959134058671$$04579375912149901004$$01928746938347503619$$02669796356526755652$$02465214312496607341$$02863069004461608889$$02389476725944600535";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
