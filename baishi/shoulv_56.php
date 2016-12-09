<?php
require_once("shoulv_api.php");
class shoulu_56 extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://seo.hd.56.com/56api/bdvideo.do?url=";
	public $site ="56.com";
	public $site_name ="56";
	public $fileInputUrls ="data/urls_56.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
