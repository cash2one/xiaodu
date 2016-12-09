<?php
require_once("shoulv_api.php");
class shoulu_le_all extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://xml.coop.le.com/forbaidu?example=";
	public $site ="le.com";
	public $site_name ="乐视网";
	public $fileInputUrls ="data/urls_le.com.all";
	public $needRelLink = true;
	public $hotRelLinkSigns = "04434820855721784073$$04200414060483724938$$04657673544730725434$$04631932804999362623$$04459669316040206890$$04811962565537483934$$04310634118359754791$$04755227262948451911$$04655905418345793624$$04523480873508264580";
	public $useInnerUrl = true;
	public $sleepInter = 1000;
}

?>
