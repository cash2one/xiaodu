<?php
require_once("shoulv_api.php");
require_once("shoulv_hbwt.php");
require_once("shoulv_baidujiaoyu.php");
require_once("shoulv_aipai.php");
require_once("shoulv_kuakao.php");
require_once("shoulv_beva.php");
require_once("shoulv_huatu.php");
require_once("shoulv_chuanke.php");
require_once("shoulv_le.php");
require_once("shoulv_le_all.php");
require_once("shoulv_ku6.php");
require_once("shoulv_baomihua.php");
require_once("shoulv_baomihuaall.php");
require_once("shoulv_pptv.php");
require_once("shoulv_pptvall.php");
require_once("shoulv_diyisp.php");
require_once("shoulv_wasu.php");
require_once("shoulv_mytv.php");
require_once("shoulv_hunantv.php");
require_once("shoulv_v6.php");
require_once("shoulv_fun.php");
require_once("shoulv_boosj.php");
require_once("shoulv_tangdou.php");
require_once("shoulv_yinyuetai.php");
require_once("shoulv_ctv.php");
require_once("shoulv_56.php");
require_once("shoulv_yy.php");

$site=$argv[1];
echo "site:$site \n";
if($site == "jiaoyu.baidu.com"){
	$runner = new shoulu_baidujiaoyu();
	$runner->isDebug = true;
	$runner->useInnerUrl = true;
}else if($site == "hbtv.com.cn"){
	$runner = new shoulu_hbwt();
	$runner->isDebug = true;
}else if($site == "aipai.com"){
	$runner = new shoulu_aipai();
	$runner->isDebug = true;
}else if($site == "www.kuakao.com"){
	$runner = new shoulu_kuakao();
	$runner->isDebug = true;
}else if($site == "g.beva.com"){
	$runner = new shoulu_beva();
	$runner->isDebug = true;
}else if($site == "v.huatu.com"){
	$runner = new shoulu_huatu();
	$runner->isDebug = true;
}else if($site == "www.chuanke.com"){
	$runner = new shoulu_chuanke();
	$runner->isDebug = true;
}else if($site == "le.com"){
	$runner = new shoulu_le();
	$runner->isDebug = true;
}else if($site == "le.com.all"){
	$runner = new shoulu_le_all();
	$runner->isDebug = true;
}else if($site == "ku6.com"){
	$runner = new shoulu_ku6();
	$runner->isDebug = true;
}else if($site == "baomihua.com"){
	$runner = new shoulu_baomihua();
	$runner->isDebug = true;
}else if($site == "baomihuaall.com"){
	$runner = new shoulu_baomihuaall();
	$runner->isDebug = true;
}else if($site == "pptv.com"){
	$runner = new shoulu_pptv();
	$runner->isDebug = true;
}else if($site == "pptvall.com"){
	$runner = new shoulu_pptvall();
	$runner->isDebug = true;
}else if($site == "v1.cn"){
	$runner = new shoulu_diyisp();
	$runner->isDebug = true;
}else if($site == "wasu.cn"){
	$runner = new shoulu_wasu();
	$runner->isDebug = true;
}else if($site == "mytv365.com"){
	$runner = new shoulu_mytv();
	$runner->isDebug = true;
}else if($site == "hunantv.com"){
	$runner = new shoulu_hunantv();
	$runner->isDebug = true;
}else if($site == "boosj.com"){
	$runner = new shoulu_boosj();
	$runner->isDebug = true;
}else if($site == "fun.tv"){
	$runner = new shoulu_fun();
	$runner->isDebug = true;
}else if($site == "v.6.cn"){
	$runner = new shoulu_v6();
	$runner->isDebug = true;
}else if($site == "kuwo.cn"){
	$runner = new shoulu_kuwo();
	$runner->isDebug = true;
}else if($site == "tangdou.com"){
	$runner = new shoulu_tangdou();
	$runner->isDebug = true;
}else if($site == "yinyuetai.com"){
	$runner = new shoulu_yinyuetai();
	$runner->isDebug = true;
}else if($site == "ctvplayer.people.cn"){
	$runner = new shoulu_ctv();
	$runner->isDebug = true;
}else if($site == "56.com"){
	$runner = new shoulu_56();
	$runner->isDebug = true;
}else if($site == "yy.com"){
        $runner = new shoulu_yy();
        $runner->isDebug = true;
}else{
	exit("site not surported now!\n");
}

$runner->run();

?>
