<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");


$data_videomap = "./data/data_from_videomap";
$data_sql_videomap = "./data/sql_from_videomap";

#mysql connect
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if ($status != ErrorNo::$RET_SUCCESS ){
        exit("failed to connect to mysql");
}

$fhandle = fopen($data_videomap, "r") or exit("open videomap file failed!");
$fwhandle = fopen($data_sql_videomap, "w") or exit("open sql_videomap file failed!");
while(false != ($line = fgets($fhandle, 1024))){
	$parts = split("\t", trim($line), 14);
	if(!$parts || count($parts) != 14){
		echo "bad line: $line \n";
		var_dump($parts);
		continue;
	}
	
	$sign = creat_sign_fs64($parts[1]);
	//var_dump($sign);
	$sign64 = "".$sign[2];
	//echo "debug: sign64-ori $sign64 \n";
	//var_dump($sign64);
	$sign64 = str_replace("-","0",$sign64);
	$tblNum =(($sign[0] + $sign[1]) % 64) + 1;
	$cmtMainInsert = "insert into tbl_video_$tblNum set title='".$parts[0]."', play_link='".$parts[1]."', real_link='".$parts[2]."', file_type=".$parts[3].", image_link='".$parts[4]."', duration=".$parts[5].", time_publish=from_unixtime(".$parts[6].") , site = '".$parts[7]."', site_name='".$parts[8]."', image_sign='".$parts[9].",".$parts[10]."', tags='".$parts[11]."', categorys='".$parts[12]."', link_sign1=".$sign[0].", link_sign2=".$sign[1].", play_link_sign64='".$sign64."', time_opt=now() ; ";
	$cmtMainUpdate = "update tbl_video_$tblNum set title='".$parts[0]."', real_link='".$parts[2]."', file_type=".$parts[3].", image_link='".$parts[4]."', duration=".$parts[5].", time_publish=from_unixtime(".$parts[6].") , site = '".$parts[7]."', site_name='".$parts[8]."', image_sign='".$parts[9].",".$parts[10]."', tags='".$parts[11]."', categorys='".$parts[12]."', time_opt=now() where link_sign1=".$sign[0]." and link_sign2=".$sign[1]." ; ";
        echo "cmt-insert: $cmtMainInsert\n";
        echo "cmt-update: $cmtMainUpdate\n";
	fwrite($fwhandle, $cmtMainInsert);
	fwrite($fwhandle, "\n");
	fwrite($fwhandle, $cmtMainUpdate);
	fwrite($fwhandle, "\n");
	//continue;
	$statusMainInsert = $originDB->oprationDB($cmtMainInsert);
	$statusMainUpdate = $originDB->oprationDB($cmtMainUpdate);
	if($statusMainInsert === ErrorNo::$RET_MYSQL_ERROR){
		echo"play link may be dup:".$parts[1]." \n";
	}
}

fclose($fhandle);
fclose($fwhandle);

?>
