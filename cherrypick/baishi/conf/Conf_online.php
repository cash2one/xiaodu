<?php
class MolaConfig
{
	public static $PrecmIp="10.36.120.39";
//	public static $PrecmIp="10.81.35.22";
	public static $PrecmPort="8766";
	public static $CheckUploadRetryTimes=10;
	public static $ImageUrl="http://i1.baidu.com/it/u=%s&fm=93";
	//public static $ImageUrl=array("http://t1.baidu.com/it/u=%s&fm=93","http://t2.baidu.com/it/u=%s&fm=93","http://t3.baidu.com/it/u=%s&fm=93");
	public static $CheckUploadIntervalInMS=100;
}

class DBConfig
{
	//online -- no
	public static $onlinedbhost = 'cq01-image-rdtest1004.vm.baidu.com:3308';
	public static $onlinedbuser = 'root';
	public static $onlinedbpass = 'MhxzKhl';
	public static $onlinedbname = 'game';
	public static $onlinedbtable_mobilegame_info= 'mobilegame_info';
	
	// transfer -- jianzhou
	//public static $origindbhost = '10.81.52.7:4001';
	public static $origindbhost = '10.42.8.95:6145';
	public static $origindbuser = 'video_yingshi_yu';
	public static $origindbpass = 'qmyOzEPruA1K';
	public static $origindbname = 'video_yingshi';
}

?>
