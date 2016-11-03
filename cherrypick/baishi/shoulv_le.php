<?php
require_once("shoulv_api.php");
class shoulu_le extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://xml.coop.letv.com/forbaidu?example=";
	public $site ="le.com";
	public $site_name ="乐视网";
	public $fileInputUrls ="data/urls_le.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
