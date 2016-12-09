<?php
require_once("shoulv_baidujiaoyu.php");

$runner = new shoulu_baidujiaoyu();
$runner->init();
$runner->isDebug = true;

$fname = $argv[1];
$fhurls = fopen($fname,"r");
if (!$fhurls){
    exit("failed to open file[$fname]");
}
while(($line = fgets($fhurls, 512))!=false){
	list($url, $c1, $c2, $c3) = explode("\t", $line);
	$sign = creat_sign_fs64(trim($url));
	$sign64 = str_replace("-","0",$sign[2]);
	
	$c3 = trim($c3);
	$category = $runner->categoryOfBaishiMap($c1,$c2,$c3);
	if(strlen($category)<1){
		echo"no map [$c1,$c2,$c3] [$category] line:$line";
	}else{
		echo"get category [$c1,$c2,$c3] map: $category url[$url] sign64[$sign64] \n";
	}
	$runner->saveCategoryAsTag($category, $sign64);

}

?>











