<?php
require_once("shoulv_api.php");
class shoulu_boosj extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://type.boosj.com/forbaidu.html?url=";
	public $site ="boosj.com";
	public $site_name ="播视网";
	public $fileInputUrls ="data/urls_boosj.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
