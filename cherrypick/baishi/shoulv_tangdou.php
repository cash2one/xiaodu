<?php
require_once("shoulv_api.php");
class shoulu_tangdou extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://www.tangdou.com/api/baiduvideo.php?url=";
	public $site ="tangdou.com";
	public $site_name ="糖豆网";
	public $fileInputUrls ="data/urls_tangdou.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
