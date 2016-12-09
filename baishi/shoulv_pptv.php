<?php
require_once("shoulv_api.php");
class shoulu_pptv extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://api2.v.pptv.com/api/baiduapi/play.json?link=";
	public $site ="pptv.com";
	public $site_name ="pptv";
	public $fileInputUrls ="data/urls_pptv.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "6999598201476232100$$08939744248948347367$$1796662868626715355$$7475746327201492421$$2829105744900974576$$08586134227776853286$$6898096860583226836$$4770089281751352790$$1222812785052765600$$7625590371000323972";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
