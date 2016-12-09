<?php
header("content-Type: text/html; charset=utf-8");

$api_site = array(
    'v.6.cn'      => 'http://v.6.cn/api/getVideoInfo.php?url=', 
    'pptv.com'    => 'http://api2.v.pptv.com/api/baiduapi/play.json?link=',
    '56.com'      => 'http://api.56.com/api/bdvideo.php?url=',
    'ku6.com'     => 'http://recv.ku6.com/baiduapi.htm?url=',
    'ifeng.com'   => 'http://dyn.v.ifeng.com/baiduVideo/getVideoInfo?vlink=',
    'iqiyi.com'   => 'http://expand.video.qiyi.com/api/fb?apiKey=cf18bf9df4124ca5b98859b9f94995c6&playurl=',
    'aipai.com'   => 'http://www.aipai.com/api/share_video.php?sid=baidu&key=15effc88d673e39fd99b6debefe98e84&url=',
    'kankan.com'  => 'http://api.kankan.com/for_baidu_v2.php?url=',
    'tangdou.com' => 'http://www.tangdou.com/api/baiduvideo.php?url=',
    'yinyuetai.com' => 'http://api.yinyuetai.com/api/baidu/short-video?currentPage=',
    'baomihua.com'  => 'http://vifo.interface.baomihua.com/interfaces/getbaiduvideo.ashx?vId=0&url=',
    'letv.com'    => 'http://xml.coop.letv.com/forbaidu?example=',
    'sina.com.cn'    => 'http://video.sina.com.cn/interface/videoListForBaidu.php?url=',
    'kankanews.com' => 'http://interface.kankanews.com/kkapi/baidu/newvideo.php?m=GET_VIDEO_CONTENT&url=',
    'v1.cn' => 'http://ynews.v1.cn/news/rec-news-fbd/?url=',
    'boosj.com' => 'http://type.boosj.com/forbaidu.html?url=',
    'pps.tv' => 'http://i.ipd.pps.tv/web/getBDVideoRec.php?url=',
    'sohu.com' => 'http://api2.tv.sohu.com/baiduvideo/info.json?api_key=e479b6f729131d336afea961629e5084&url=',
    'm1905.com' => 'http://www.m1905.com/api/forbaidu/?from=',
    'cntv.cn' => 'http://tv.cntv.cn/api/Videoframe/videoinfo?url=',
    'joy.cn' => 'http://www.joy.cn/forbaidu?url=',
    'pinshan.com' => 'http://www.pinshan.com/tobaidu/?url=',
    'mytv365.com' => 'http://subject.mytv365.com/mytv365/forbaidu.do?address=',
    '17173.com' => 'http://17173.tv.sohu.com/port/forbaidu.php?url=',
    '163.com' => 'http://so.v.163.com/share/baidu.htm?url=',
    'wasu.cn' => 'http://api.wasu.cn/Vod/baidu/square?playurl=',
    'fun.tv' => 'http://api.fun.tv/api/baidu_video/?res=',
    'baofeng.com' => 'http://fapi.hd.baofeng.com/baidu?url=',
    'hbtv.com' => 'http://app.hbtv.com.cn/baiduvideo.php?example=',
    's1979.com' => 'http://cms.s1979.com/plus/forbaidu.php?url=',
    'jxntv.com' => 'http://www.jxntv.cn/forbaidu/?url=',
    '1905.com' => 'http://www.1905.com/api/interface/baidu_video_resolve.php?url=',
    'cztv.com' => 'http://me.cztv.com/xml/baiduhttp/?site=',
    'people' => 'http://st01-video-liulan.st01.baidu.com:8070/coop/?url=',
    'bilibili.com' => 'http://api.bilibili.com/baidu_view?url=',
    //'hunantv.com' => 'http://ext.api.hunantv.com/short/baidu.php?url=',
    //'kuwo' => 'http://kuwo.cn/yy/yueku/forbaidu.jsp?url=',    
    //'miaopai.com' => 'http://cq02-c1-video-mprd1.cq02.baidu.com:8070/coop/?site=miaopai&url=',
    //'39yst.com' => 'http://cq02-c1-video-mprd1.cq02.baidu.com:8070/coop/?site=39yst&url=',
    //'xiaokaxiu.com' => 'http://cq02-c1-video-mprd1.cq02.baidu.com:8070/coop/?site=xiaokaxiu&url=',
);

 echo json_encode(array_keys($api_site));

?>

