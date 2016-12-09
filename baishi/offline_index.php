<?php
header("content-Type: text/html; charset=utf-8");
require_once("shoulv_api.php");


$url   = $argv[1];
$site   = $argv[2];

$api_site = array(
    'v6'      => 'http://v.6.cn/api/getVideoInfo.php?url=',
    'pptv'    => 'http://api2.v.pptv.com/api/baiduapi/play.json?link=',
    '56'      => 'http://seo.hd.56.com/56api/bdvideo.do?url=',
    'ku6'     => 'http://recv.ku6.com/baiduapi.htm?url=',
    'ifeng'   => 'http://dyn.v.ifeng.com/baiduVideo/getVideoInfo?vlink=',
    'iqiyi'   => 'http://expand.video.qiyi.com/api/fb?apiKey=cf18bf9df4124ca5b98859b9f94995c6&playurl=',
    'aipai'   => 'http://www.aipai.com/api/share_video.php?sid=baidu&key=15effc88d673e39fd99b6debefe98e84&url=',
    'kankan'  => 'http://api.kankan.com/for_baidu_v2.php?url=',
    'tangdou' => 'http://www.tangdou.com/api/baiduvideo.php?url=',
    'yinyuetai' => 'http://api.yinyuetai.com/api/baidu/short-video?currentPage=',
    'baomihua'  => 'http://vifo.interface.baomihua.com/interfaces/getbaiduvideo.ashx?vId=0&url=',
    'letv'    => 'http://xml.coop.letv.com/forbaidu?example=',
    'sina'    => 'http://video.sina.com.cn/interface/videoListForBaidu.php?url=',
    'kankanews' => 'http://interface.kankanews.com/kkapi/baidu/newvideo.php?m=GET_VIDEO_CONTENT&url=',
    'v1' => 'http://ynews.v1.cn/news/rec-news-fbd/?url=',
    'boosj' => 'http://type.boosj.com/forbaidu.html?url=',
    'pps' => 'http://i.ipd.pps.tv/web/getBDVideoRec.php?url=',
    'sohu' => 'http://api2.tv.sohu.com/baiduvideo/info.json?api_key=e479b6f729131d336afea961629e5084&url=',
    'm1905' => 'http://www.m1905.com/api/forbaidu/?from=',
    'cntv' => 'http://tv.cntv.cn/api/Videoframe/videoinfo?url=',
    'joy' => 'http://www.joy.cn/forbaidu?url=',
    'pinshan' => 'http://www.pinshan.com/tobaidu/?url=',
    'mytv365' => 'http://subject.mytv365.com/mytv365/forbaidu.do?address=',
    '17173' => 'http://17173.tv.sohu.com/port/forbaidu.php?url=',
    '163' => 'http://so.v.163.com/share/baidu.htm?url=',
    'wasu' => 'http://api.wasu.cn/Vod/baidu/square?playurl=',
    'fun' => 'http://api.fun.tv/api/baidu_video/?res=',
    'baofeng' => 'http://fapi.hd.baofeng.com/baidu?url=',
    'hbtv' => 'http://app.hbtv.com.cn/baiduvideo.php?example=',
    's1979' => 'http://cms.s1979.com/plus/forbaidu.php?url=',
    'jxntv' => 'http://www.jxntv.cn/forbaidu/?url=',
    '1905' => 'http://www.1905.com/api/interface/baidu_video_resolve.php?url=',
    'cztv' => 'http://me.cztv.com/xml/baiduhttp/?site=',
    'people' => 'http://st01-video-liulan.st01.baidu.com:8070/coop/?url=',
    'bilibili' => 'http://api.bilibili.com/baidu_view?url=',
    'hunantv' => 'http://ext.api.hunantv.com/short/baidu.php?url=',
    'kuwo' => 'http://kuwo.cn/yy/yueku/forbaidu.jsp?url=',
);

if((is_null($url) || empty($url)) && (is_null($site) || empty($site))){
    echo('{"status":-1}');
}elseif ((!empty($url))){
    if (array_key_exists($site, $api_site)){
        $api_url = $api_site[$site];
        $runner = new shoulu_api();
        $runner->apiFormat=$api_url;
        $runner->site =$site;
        $runner->useInnerUrl =true;
        $runner->needRelLink =true;
        $returninfo = $runner->processUrl($url);
        echo $returninfo;
    }else{
        echo('{"status":-2}');
    }
}
?>