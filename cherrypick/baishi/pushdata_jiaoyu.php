<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

$filename = $argv[1];
//mysql connect
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if ($status != ErrorNo::$RET_SUCCESS ){
    exit("failed to connect to mysql");
}

$fhandle = fopen($filename, "r");
if (!$fhandle){
    exit (" failed to open url file[$filename]");
}
$lineCount = 0;
while(false !== ($line = fgets($fhandle))){
    $lineCount += 1;
    $line = trim($line);
    echo "now process at[$lineCount]\n";
    
    list($title,$category,$duration,$imglink,$realLink, $tags,$desc,$playLink,$pubtime,$albumName, $albumLink,$albumDesc,$albumIdx,$site,$siteName, $bcsUrl) = explode("\t",$line,16);
    if(strlen($albumLink) < 1){
        $albumLink = $albumName;
    }
    //insert into yingshi_video_ori
    $cmt1 = "replace into yingshi_video_ori set site='$site', categorys='$category', album_name='$albumName', album_link='$albumLink',album_description='$albumDesc', album_index='$albumIdx',title='$title', description='$desc',play_link='$playLink', image_links='$imglink',tags='$tags', publish_time='$pubtime', insert_time=now(), real_links='$realLink',duration='$duration', op='add' ; ";
    echo "$cmt1\n";
    $statusMain = $originDB->oprationDB($cmt1);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data to yingshi_video_ori failed! cmt:$cmt1 \n";
    }
    //insert into yingshi_video_convert
    if(strlen($bcsUrl) > 7){
        $cmt2 = "replace into yingshi_video_convert set real_link='$realLink', bcs_url='$bcsUrl', format='9999'; ";
        $statusMain = $originDB->oprationDB($cmt2);
        if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
            echo "save data to yingshi_video_convert failed! cmt:$cmt2 \n";
        }
        echo "$cmt2\n";
    }
    continue;
    //insert into tbl_album
    $cmt3 = "replace into tbl_album set title='$albumName', description='$albumDesc', link='$albumLink', insert_time=now();";
    $statusMain = $originDB->oprationDB($cmt3);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data to tbl_album failed! cmt:$cmt3 \n";
    }
    $aid = mysql_insert_id();
    echo "$cmt3\n";
    //insert into tbl_video
    $cmt4 = "replace into tbl_video set play_link_md5='md5(play_link)', site='$site', title='$title', image_link='', duration='$duration',description='$desc',pub_time='$pubtime',play_link='$playLink',aid='$aid',insert_time=now();";
    $statusMain = $originDB->oprationDB($cmt4);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data to tbl_video failed! cmt:$cmt4 \n";
    }
    $vid = mysql_insert_id();
    echo "$cmt4\n";
    //insert into tbl_video_file
    $cmt5 = " replace into tbl_video_file set vid='$vid', file_type='3083', file_url='$realLink', insert_time=now();";
    $statusMain = $originDB->oprationDB($cmt5);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data to tbl_video failed! cmt:$cmt5 \n";
    }
    echo "$cmt5\n";
    //insert into tbl_video_tag
    $cmttag = "replace into tbl_video_tag set vid='$vid', tag='$category' ;";
    $statusMain = $originDB->oprationDB($cmttag);
    if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
        echo "save data to tbl_video failed! cmt:$cmttag \n";
    }
    echo "$cmttag\n";
}
?>