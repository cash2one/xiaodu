#!/bin/bash
#set -x

sign1="$1"
sign2="$2"
sign1sign2="$3"
if [ "$sign1sign2" != "" ]
then
	sign1=`echo "$sign1sign2" | awk -F',' '{print $1}'`
	sign2=`echo "$sign1sign2" | awk -F',' '{print $2}'`
	
fi

echo "$sign1sign2"

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
else
cmd="$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e \"select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G\""
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
fi

echo $cmd
echo
echo "spider_url is:
$result"

echo "************************************************"

if((`expr $index % 2` == 0))
then
result=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
else
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
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
