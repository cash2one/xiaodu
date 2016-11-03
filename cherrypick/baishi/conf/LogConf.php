<?php
/***************************************************************************
 * 
 * Copyright (c) 2013 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file LogConf.php
 * @author wangxuan03(com@baidu.com)
 * @date 2013/04/24 10:33:09
 * @brief 
 *  
 **/
//log
ini_set('date.timezone','Asia/Shanghai');
include ('./lib/log.class.php');
//require './log.class.php'; 
Log::set_size(1024*1024*10); 
#$url='http://'.$_SERVER['SERVER_NAME'].':'.$_SERVER["SERVER_PORT"].$_SERVER["REQUEST_URI"];
define('DS', DIRECTORY_SEPARATOR); 
define('LOG_PATH','/home/img/game_box/mobilegame_info/log/');





/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
?>
