<?php

require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

$filedead = $argv[1];
$site = $argv[2];

//mysql connect
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if ($status != ErrorNo::$RET_SUCCESS ){
        exit("failed to connect to mysql");
}

$fhandle = fopen($filedead, "r");
if (!$fhandle){
    exit (" failed to open url file[$filedead]");
}
$lineCount = 1;
while(false !== ($line = fgets($fhandle, 1024))){
	echo "now process at[$lineCount] \n";
	$lineCount += 1;
	$line = trim($line);
	list($flag_dead, $url) = explode("\t", $line);
	$sign = creat_sign_fs64($url);
	$sign64 = str_replace("-","0",$sign[2]);
	$tblNumMain = (($sign[0] + $sign[1]) % 64) + 1;

	$cmtMain = " update tbl_video_$tblNumMain set flag_dead=$flag_dead where link_sign1='".$sign[0]."' and link_sign2='".$sign[1]."' and site='$site';";
	echo "cmt: $cmtMain\n";
	$statusMain = $originDB->oprationDB($cmtMain);
	if($statusMain === ErrorNo::$RET_MYSQL_ERROR){
		echo"play link may be dup $line\n";
	}
}
return 0;

?>
