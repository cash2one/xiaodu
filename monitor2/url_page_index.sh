#!/bin/bash
#set -x

echo "<br><a href=http://tc-video-ld00.tc.baidu.com:8086/>首页</a><br><FORM ACTION="/cgi-bin/q_url.cgi" METHOD="GET">
<p>
<input  name='url' size=60 />
<INPUT TYPE=SUBMIT VALUE="OK" />
</p>
</FORM><br>"
#为php提供库路径
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/video/php/lib/php/extensions/no-debug-non-zts-20060613

if [ $# -ne 1 ]
then

	echo "./url_page_index.sh url"
	exit 
fi

url=$1

echo "原始url为 $url"
#小海哥的解密
url3=`/home/video/php/bin/php /home/video/q_url/fuck.php "$url" `

num=`echo "$url3" | wc -l`
echo $num
if [ $num -eq 2 ]
then
	url2=`echo "$url3" | tail -1`
	url=$url2
fi
echo "解密url为 $url2"


url=${url# }
url=${url% }

echo $url | grep '^[0-9]\+-[0-9]\+$' 1>/dev/null 2>&1

[ $? -eq 0 ] && {
    sign1=`echo $url | cut -f1 -d\-`
    sign2=`echo $url | cut -f2 -d\-`
} || {
    sign1=`/home/video/q_url/print_sign $url | awk '{print $1}'`
    sign2=`/home/video/q_url/print_sign $url | awk '{print $2}'`
}

sign1=`echo $sign1`
sign2=`echo $sign2`

sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`

MYSQL_BIN=/home/video/database/mysql/bin/mysql
echo "sign1 is :"$sign1
echo "sign2 is :"$sign2
echo $index
if((`expr $index % 2` == 0))
then
cmd="$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e \"select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G\""
result=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
imgsign1=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video --skip-column-names -e "select image_sign1,image_sign2,player_title from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2"`
echo "$imgsign1" | awk -F'\t' '{print "<img src=http://t1.baidu.com/it/u="$1","$2"&fm=20>"$3}' 

else
cmd="$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e \"select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G\""
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
imgsign1=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video --skip-column-names -e "select image_sign1,image_sign2,player_title from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2"`
echo "$imgsign1" | awk -F'\t' '{print "<img src=http://t1.baidu.com/it/u="$1","$2"&fm=20>"$3}' 
#<img src=http://t3.baidu.com/it/u="$1","$2"&fm=20 >"'

fi

echo $cmd
echo
echo "spider_url is:
$result"

echo "************************************************"

if((`expr $index % 2` == 0))
then
result=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
imgsign1=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video --skip-column-names -e "select image_sign1,image_sign2,player_title from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2"`
echo "$imgsign1" | awk -F'\t' '{print "<img src=http://t1.baidu.com/it/u="$1","$2"&fm=20>"$3}' 
else
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
imgsign1=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video --skip-column-names -e "select image_sign1,image_sign2,player_title from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2"`
echo "$imgsign1" | awk -F'\t' '{print "<img src=http://t1.baidu.com/it/u="$1","$2"&fm=20>"$3}' 
fi
echo "videomap_url is:
$result"

echo "************************************************"

result=`$MYSQL_BIN -h 10.92.133.17 -P3309 -uvideo -pvideo short_video -e "select *,from_unixtime(crt_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
echo "gbs_url is:
$result"


#echo "************************************************"

#result=`$MYSQL_BIN -h 10.26.26.87 -P4200 -uvideo_w -pNs09NHJL video -e "select *,from_unixtime(crt_time) from possible_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "possible_url is:
#$result"

#echo "************************************************"

#result=`$MYSQL_BIN -h 10.26.26.87 -P4200 -uvideo_w -pNs09NHJL video -e "select *,from_unixtime(crt_time) from normal_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "normal_url is:
#$result"

#echo "************************************************"

#result=`$MYSQL_BIN -h 10.81.50.211 -u video -pvideo video -e "select *,from_unixtime(crt_time) from sobar_url${index} where
#result=`$MYSQL_BIN -h 10.26.26.87 -u video -pvideo video -e "select *,from_unixtime(crt_time) from sobar_url${index} where
# link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "sobar_url is:
#$result" 
exit 0
