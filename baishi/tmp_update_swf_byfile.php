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
if (!$fhandle){
    exit (" failed to open url file[$fileinsert]");
}
$lineCount = 1;
while(false !== ($line = fgets($fhandle, 1024))){
	echo "now process at[$lineCount] \n";
	$lineCount += 1;
	$line = trim($line);
	list ($url,$swf) = explode("\t",$line);
	$sign = creat_sign_fs64($url);
	$tblNumMain =(($sign[0] + $sign[1]) % 64) + 1;
	$cmtMain = " update tbl_video_$tblNumMain set real_link='$swf' where play_link='".$url."' ;";
	echo "cmt: $cmtMain\n";
	$statusMain = $originDB->oprationDB($cmtMain);
	if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
		echo"play link may be dup $line\n";
	}
}

?>
