<?php
require_once("shoulv_api.php");
class shoulu_hunantv extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://ext.api.hunantv.com/short/baidu.php?url=";
	public $site ="hunantv.com";
	public $site_name ="芒果TV";
	public $fileInputUrls ="data/urls_hunantv.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "6075879032308222821$$5858252614100478822$$5257352290980821066$$5734942973485152272$$5376134692527923160$$5491327880027461389$$5328455968447569712$$5044558376756422292$$5281864343552239809$$5389786091407366999";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
