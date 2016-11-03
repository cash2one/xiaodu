<?php
require_once("shoulv_api.php");
class shoulu_beva extends shoulu_api {

	public $apiFormat ="http://g.beva.com/kan/baidu/item?from=";
	public $site ="g.beva.com";
	public $site_name ="贝瓦网";
	public $fileInputUrls ="data/urls_g.beva.com";
	public $needRelLink = true;
	public $relItems ="relatedStream";
	public $hotRelLinkSigns = "0231677206174668258$$07413555981252672029$$7377255004481779085$$02615020107983407047$$1031808723220287101$$7625985938832952256$$7330799107188738798$$01591927338806027159$$1585924471885847059$$02320766705263870181$$04373092668851452626$$08395857596595809324$$4103537198894119099";
	public $useInnerUrl = true;
}

?>
