<?php
require_once("shoulv_api.php");
class shoulu_baomihuaall extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://vifo.interface.baomihua.com/interfaces/getbaiduvideo.ashx?vId=0&url=";
	public $site ="baomihua.com";
	public $site_name ="爆米花";
	public $fileInputUrls ="data/urls_baomihuaall.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "05098976520224310712$$05206869809626020567$$05492465884836587827$$0471562215339079307$$587395635701812163$$0463009548135870306$$04620950512547361784$$05616444058645062043$$05609834743916570173$$0116003747081586801";
	public $useInnerUrl = true;
	public $sleepInter = 100000;
}

?>
