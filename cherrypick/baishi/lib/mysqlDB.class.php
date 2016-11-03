<?php
#require_once("lib/mcpack.class.php");
#require_once("conf/Conf.php");	
require_once("lib/errorno.class.php");
@set_time_limit(0);
class SendMysql
{
	var $_connectInfo;
	public function connectMysql($dbhost,$dbuser,$dbpass,$dbname)
	{
		$this->_connectInfo = mysql_connect($dbhost,$dbuser,$dbpass,true);
		if (!$this->_connectInfo) 
		{
			return ErrorNo::$RET_MYSQL_ERROR;
		}    
		$useDBname="use ".$dbname;
		$ret=mysql_query("$useDBname");
		if(!$ret)
		{    
			return ErrorNo::$RET_MYSQL_ERROR;
		}    
		$ret=mysql_query("set names 'utf8'");
		if(!$ret)
		{    
			return ErrorNo::$RET_MYSQL_ERROR;
		}    
		return ErrorNo::$RET_SUCCESS;
	}
	public function closeMysql()
	{
		if($this->_connectInfo)
		{
			mysql_close($this->_connectInfo);
		}
	}
	public function oprationDB($sql_str)
	{
		if(!isset($sql_str))
		{    
			return ErrorNo::$RET_MYSQL_ERROR;
		}    
		$result = mysql_query($sql_str);
		if(!$result)
		{    
			return ErrorNo::$RET_MYSQL_ERROR;
		}    
		return $result; 
	}
	public function insertAndRetureId($sql_str)
	{
		if(!isset($sql_str))
                {
                        return ErrorNo::$RET_MYSQL_ERROR;
                }
                $result = mysql_query($sql_str);
                if(!$result)
                {
                        return ErrorNo::$RET_MYSQL_ERROR;
                }
		$id = 0;
		if($id = mysql_insert_id())
		{
			return $id;
		}
		return ErrorNo::$RET_MYSQL_ERROR;
	}
}
?>
