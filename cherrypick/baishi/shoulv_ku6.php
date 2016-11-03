<?php
require_once("shoulv_api.php");
class shoulu_ku6 extends shoulu_api {

	public $mapCategoryLevel1 = array(
	);
	public $mapCategoryLevel2 = array(
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://recv.ku6.com/baiduapi.htm?url=";
	public $site ="ku6.com";
	public $site_name ="酷6网";
	public $fileInputUrls ="data/urls_ku6.com";
	public $needRelLink = true;
	public $hotRelLinkSigns = "7324020995200008780$$07640893537981200083$$1944553286650374739$$01158174534533952758$$2631750101763256489$$5265013719524453158$$6748168027785021493$$9207761049378662534$$08289946146949371417$$8406111701059463921";
	public $useInnerUrl = true;
	public $sleepInter = 10000;
}

?>
