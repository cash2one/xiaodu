<?php
require_once("shoulv_api.php");
class shoulu_kuakao extends shoulu_api {

	public $apiFormat ="http://www.kuakao.com/video/forBaidu.action?url=";
	public $site ="www.kuakao.com";
	public $site_name ="跨考";
	public $fileInputUrls ="data/urls_www.kuakao.com";
	public $needRelLink = true;
	public $relItems ="albumStream";
	public $hotRelLinkSigns = "2600467613221847373$$2873695797479373974$$2986074011958366939$$3245718211415647111$$3321012445284546891$$3347240217431104556$$3407046851023436052$$3407837258178395317$$3529821746827936104$$3570746712096102788";
	public $useInnerUrl = true;
}

?>
