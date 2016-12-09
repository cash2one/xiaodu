<?php
require_once("shoulv_api.php");
class shoulu_kuwo extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://www.kuwo.cn/yy/yueku/forbaidu.jsp?url=";
	public $site ="kuwo.cn";
	public $site_name ="酷我网";
	public $fileInputUrls ="data/urls_kuwo.cn";
	public $needRelLink = true;
	public $hotRelLinkSigns = "";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
