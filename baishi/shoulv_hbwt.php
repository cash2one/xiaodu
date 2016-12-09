<?php
require_once("shoulv_api.php");
class shoulu_hbwt extends shoulu_api {
	public $apiFormat = "http://app.hbtv.com.cn/baiduvideo.php?example=";
	public $site = "hbtv.com.cn";
	public $site_name = "湖北网台";
	public $fileInputUrls = "./data/urls_hbwt";
	public $needRelLink = false;
}

#$runer = new shoulu_hbwt;
#$runer->run();
?>
