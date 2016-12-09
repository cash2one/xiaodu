<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

$filename = $argv[1];
$fileRelLinks = "data/playlinks_hbwt";
$site = "hbtv.com.cn";
//$site_name = "湖北网台";
$filetype = 3078;
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
while(false !== ($line = fgets($fhandle))){
        $lineCount += 1;
    //echo "now process at[$lineCount]\n";

    list($play_link,$title,$relLinks,$reallink) = split("\t",trim($line),4);
    $sign = creat_sign_fs64($play_link);
    $sign64 = str_replace("-","0",$sign[2]);
    $tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
    $relLinkSigns = "";
    $rels = explode("$$", $relLinks);
    //var_dump($rels);
    //foreach($rels as $item){
    $cntmax = 0;
    for($idx=0,$num=count($rels);$idx<$num && $cntmax < 20;$idx++){
        $item = $rels[$idx];
        //var_dump($item);
        if(in_array($item,$validlinks)){
            $signTmp = creat_sign_fs64($item);
            $sign64tmp = str_replace("-","0",$signTmp[2]);
            $relLinkSigns = $sign64tmp."$$".$relLinkSigns;
            //echo "now the relLinkSigns:$relLinkSigns\n";
            $cntmax++;
        }else{
            //echo "no in\n";
        }
    }
    if(strlen($relLinkSigns)<5){
        echo "no rel links: $line\n";
        continue;
    }
    //$cmtMain = "replace into tbl_video_$tblNumMain set title='$title', play_link='$play_link', rel_link_sign64s='$relLinkSigns', real_link='$reallink', file_type='$filetype' ,site = '$site', site_name = '$site_name', link_sign1=".$sign[0].", link_sign2=".$sign[1].", play_link_sign64='".$sign64."', time_opt=now() ; ";
    $cmtMain = "update tbl_video_$tblNumMain set rel_link_sign64s='$relLinkSigns',time_opt=now() where play_link='$play_link'; ";
    echo "cmt-video: $cmtMain\n";
    $statusMain = $originDB->oprationDB($cmtMain);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data failed! cmt:$cmtMain \n";
    }else{
        $vid = mysql_insert_id();
        continue;
        $cmtVideofile = "replace into tbl_video_file set vid=$vid, play_link_sign64='$sign64', file_type='$filetype', file_url='$reallink', insert_time=now(); ";
        echo "cmt-vfile: $cmtVideofile\n";
        $statusMain = $originDB->oprationDB($cmtVideofile);
        if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
            echo "insert vfile failed!\n";
        }
    }
}
fclose($fhandle);

?>
