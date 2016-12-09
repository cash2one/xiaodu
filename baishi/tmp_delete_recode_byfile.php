<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

$fileinsert = $argv[1];

//mysql connect
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if ($status != ErrorNo::$RET_SUCCESS ){
        exit("failed to connect to mysql");
}

$fhandle = fopen($fileinsert, "r");
if ( !$fhandle ){
    exit (" failed to open url file[$fileinsert]");
}
$lineCount = 1;
while(false !== ($line = fgets($fhandle, 1024))){
	echo "now process at[$lineCount] \n";
	$lineCount += 1;
	$line = trim($line);
	list ($sign1,$sign2,$play_link) = explode("\t",$line);
	$tblNumMain =(($sign1 + $sign2) % 64) + 1;
	//$cmtMain = " update tbl_video_$tblNumMain set flag_dead=1 where link_sign1=$sign1 and link_sign2=$sign2 ;";
	$cmtMain = " delete from tbl_video_$tblNumMain where link_sign1=$sign1 and link_sign2=$sign2 ;";
	echo "cmt: $cmtMain\n";
	$statusMain = $originDB->oprationDB($cmtMain);
	if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
		echo"play link may be dup $line\n";
	}
}

?>
