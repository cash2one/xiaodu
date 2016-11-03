<?php
require_once("shoulv_api.php");
require_once("shoulv_hbwt.php");
require_once("shoulv_baidujiaoyu.php");
require_once("shoulv_chuanke.php");

$site=$_GET["site"];
$url=$_GET["url"];

if($site == "chuanke.com" && strlen($url) > 7){
	$runner = new shoulu_chuanke;
	$runner->isDebug = false;
	#$runner->isDebug = true;
	#$runner->needUrlDecode = true;
	$runner->mustHaveRelLink = true;
	$runner->useInnerUrl = true;
	echo $runner->getUrlInfoDb($url);
}else if($site == "hbtv.com.cn" && strlen($url) > 7){
	$runner = new shoulu_hbwt;
	echo $runner->getUrlInfoDb($url);
}else{
	$retval = array();
	$retval["status"] = 5;
	$retval["msg"] = "site or url invalid! site[$site] url[$url]";
	echo json_encode($retval);
}

?>
