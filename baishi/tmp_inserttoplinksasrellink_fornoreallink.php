<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

$filename = $argv[1];
$fileRelLinks = $argv[2];
//mysql connect
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if ($status != ErrorNo::$RET_SUCCESS ){
        exit("failed to connect to mysql");
}
//all rel links
$fhandleRel = fopen($fileRelLinks, "r");
if (!$fhandleRel){
    exit (" failed to open url file[$filename]");
}
$validlinks = array();
while(false !==($line = fgets($fhandleRel))){
    $cleanurl = trim($line);
    array_push($validlinks, $cleanurl);
}
fclose($fhandleRel);
//var_dump($validlinks);

$fhandle = fopen($filename, "r");
if (!$fhandle){
    exit (" failed to open url file[$filename]");
}
$lineCount = 0;
$nummax = count($validlinks);
while(false !== ($line = fgets($fhandle))){
    $lineCount += 1;
    //echo "now process at[$lineCount]\n";

    $play_link = trim($line);
    $sign = creat_sign_fs64($play_link);
    $sign64 = str_replace("-","0",$sign[2]);
    $tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
    $relLinkSigns = "";
    $rels = explode("$$", $relLinks);
    //var_dump($rels);
    $idx = rand(0,$nummax);
    echo "idx rand:$idx numax:$nummax\n";
    for($cntmax = 0;$cntmax < 20;++$cntmax){
        $idx = (++$idx) % $nummax;
        $item = $validlinks[$idx];
        //var_dump($item);
        $signTmp = creat_sign_fs64($item);
        $sign64tmp = str_replace("-","0",$signTmp[2]);
        $relLinkSigns = $sign64tmp."$$".$relLinkSigns;
        //echo "now the relLinkSigns:$relLinkSigns\n";
    }
    if(strlen($relLinkSigns)<5){
        echo "no rel links: $line\n";
        continue;
    }
    $cmtMain = "update tbl_video_$tblNumMain set rel_link_sign64s='$relLinkSigns',time_opt=now() where play_link='$play_link'; ";
    echo "cmt-video: $cmtMain\n";
    break;
    $statusMain = $originDB->oprationDB($cmtMain);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data failed! cmt:$cmtMain \n";
    }
}
fclose($fhandle);

?>
