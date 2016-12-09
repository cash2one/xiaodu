<?php 
//reques:
require_once("lib/mysqlDB.class.php");
require_once("lib/mola.class.php");
require_once("lib/errorno.class.php");
require_once("conf/Conf.php");
require_once("conf/LogConf.php");

//get all ready data: has been complessed 
$originDB=new SendMysql();
$status = $originDB->connectMysql(DBConfig::$origindbhost, DBConfig::$origindbuser, DBConfig::$origindbpass, DBConfig::$origindbname);
if($status != ErrorNo::$RET_SUCCESS){
	$originDB->closeMysql();
	exit("Unable to open mysql" );
}

$cmt_sel = "select partner as site, categorys , album_name, album_description, album_index, title, description, play_link, bcs_url as real_link, bcs_url_compress_high, '3083' as format_h, image_url, image_sign, tags, duration from tbl_video_ori_mis where v_status <= 1 and bcs_url != '' and bcs_url_compress_high != '' and play_link_sign ='' ";
/*
    $cmt_sel = "select partner as site, categorys , album_name, album_description, album_index, title, description, play_link, bcs_url as real_link, bcs_url_compress_high, '3083' as format_h, image_url, image_sign, tags, duration from tbl_video_ori_mis where v_status <= 1 and bcs_url != '' and bcs_url_compress_high != ''";// and play_link_sign ='' ";
*/
echo "cmt_sel:$cmt_sel \n";
$ret = $originDB->oprationDB($cmt_sel);
if($ret === ErrorNo::$RET_MYSQL_ERROR){
	$originDB->closeMysql();
	exit("fetch data failed!" );
}
$len_ret=mysql_num_rows($ret);
echo "get data len[$len_ret]\n";
for($idx=0; $idx<$len_ret; $idx++){
	$item = mysql_fetch_assoc($ret);
	if(!$item){
        break;
    }
	echo "idx:$idx\n";
	//push to tbl_video_XX
	$url = $item["play_link"];
	$sign = creat_sign_fs64($url);
	var_dump($sign);
	$sign64 = str_replace("-","0",$sign[2]);
	$tblNumRel = (($sign[0] + $sign[1]) % 64) + 1;
	echo"url[$url] sign64[$sign64]\n";

	//tmp delete
	echo "delete from tbl_video_$tblNumRel where play_link='".$item["play_link"]."';\n";

	$cmt_tbl = "insert into tbl_video_$tblNumRel set categorys='".$item["categorys"]."', tags='".$item["tags"]."', album_name='".$item["album_name"]."', album_index='".$item["album_index"]."', title='".$item["title"]."', play_link='".$item["play_link"]."', real_link='".$item["real_link"]."', file_type=".$item["format_h"].", image_link='".$item["image_url"]."', duration=".$item["duration"].",   site='".$item["site"]."', link_sign1=".$sign[0].", link_sign2=".$sign[1].", play_link_sign64='".$sign64."', time_opt=now() ;";
	echo "cmt_tbl:$cmt_tbl\n";
	$status = $originDB->oprationDB($cmt_tbl);
	if($status === ErrorNo::$RET_MYSQL_ERROR){
		echo "insert into tbl_video failed!\n";
	}else{
		echo "insert into tbl OK!\n";
		$cmt_convert = "insert into yingshi_video_convert set real_link='".$item["real_link"]."', bcs_url='".$item["bcs_url_compress_high"]."', format=".$item["format_h"].", real_link_md5=md5('".$item["real_link"]."'), play_link_sign='$sign64' ;";
		echo "insert into convert: $cmt_convert\n";
		$originDB->oprationDB($cmt_convert);
		$cmt_update = "update tbl_video_ori_mis set play_link_sign='$sign64' where play_link='".$item["play_link"]."' ;";
		echo "now update mis[$cmt_update]\n";
		$originDB->oprationDB($cmt_update);
		if(strlen($item["album_name"]) > 1){
			$cmt_album = "insert into tbl_album_urlsign set site='".$item["site"]."', album_name='".$item["album_name"]."', album_link='".$item["album_name"]."', album_index=".$item["album_index"].", play_link_sign64='$sign64' ;";
			echo "cmt_album:$cmt_album \n";
			$originDB->oprationDB($cmt_album);	
		}
	}
}
$originDB->closeMysql();

?>
