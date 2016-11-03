<?php
require_once("shoulv_api.php");
class shoulu_aipai extends shoulu_api {

	public $mapCategoryLevel1 = array(
		"非游戏"=>"非游戏",
		"游戏"=>"游戏",
	);
	public $mapCategoryLevel2 = array(
		"手绘"=>"手绘",
		"COSPLAY"=>"COSPLAY",
		"同人原创"=>"同人原创",
		"影视恶搞"=>"影视恶搞",
		"萌宠"=>"萌宠",
		"美食美厨"=>"美食美厨",
		"晒潮物"=>"晒潮物",
		"化妆打扮"=>"化妆打扮",
		"街拍实拍"=>"街拍实拍",
		"微电影"=>"微电影",
		"综合生活时尚"=>"综合生活时尚",
		"爱拍&九州车迷"=>"爱拍&九州车迷",
		"生活随拍"=>"生活随拍",
		"配音"=>"配音",
		"音乐原创"=>"音乐原创",
		"主播联萌"=>"主播联萌",
		"潮舞"=>"潮舞",
		"脱口秀"=>"脱口秀",
		"器乐演奏"=>"器乐演奏",
		"跑酷滑板"=>"跑酷滑板",
		"功夫"=>"功夫",
		"DJ喊麦"=>"DJ喊麦",
		"综合娱乐"=>"综合娱乐",
		"穿越火线"=>"穿越火线",
		"地下城与勇士"=>"地下城与勇士",
		"QQ飞车"=>"QQ飞车",
	);
	public $mapCategoryLevel3 = array(
	);

	public $apiFormat ="http://www.aipai.com/api/share_video.php?sid=baidu&url=";
	public $site ="aipai.com";
	public $site_name ="爱拍网";
	public $fileInputUrls ="./data/urls_aipai.com";
	public $needRelLink = true;
	public $relItems ="relatedStreams";
	public $needSaveTagUrlRel = false;
	public $needFetchFromNet = true;
	public $needSaveCategoryAstag = false;
}

?>
