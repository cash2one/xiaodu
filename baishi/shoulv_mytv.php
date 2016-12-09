<?php
require_once("shoulv_api.php");
class shoulu_mytv extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://www.mytv365.com/mytv365/forbaidu.do?address=";
	public $site ="mytv365.com";
	public $site_name ="炎黄";
	public $fileInputUrls ="data/urls_mytv365.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "04850019664580976030$$04493190938297355396$$04314776575155545079$$04612133847058562274$$04552662392677958835$$04374248029536148518$$04227245223258381505$$04701477211283936576$$04680186508643218350$$04406423966002461815";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
