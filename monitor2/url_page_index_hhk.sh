#!/bin/bash
#set -x

if [ $# -ne 1 ]
then

	echo "./url_page_index.sh url"
	exit 
fi

sign1=`~/print_sign $1 | awk '{print $1}'`
sign1=`echo $sign1`

sign2=`~/print_sign $1 | awk '{print $2}'`
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
result=`$MYSQL_BIN -h 10.23.255.128 -u video -pvideo video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
else
result=`$MYSQL_BIN -h 10.23.246.174 -u video -pvideo video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
fi
#echo "spider_url is:
#$result"

n1=`echo $result|grep "from_type"|awk -F "from_type" '{print $2}'`
#echo "************************************************"

if((`expr $index % 2` == 0))
then
result=`$MYSQL_BIN -h 10.23.255.128 -u video -pvideo video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
else
result=`$MYSQL_BIN -h 10.23.246.174 -u video -pvideo video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
fi
#echo "videomap_url is:
#$result"

n2=`echo $result|grep "crt_time"|awk -F "):" '{print $2}'`

#echo "************************************************"

result=`$MYSQL_BIN -h 10.81.50.211 -u video -pvideo video -e "select *,from_unixtime(crt_time) from possible_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "possible_url is:
#$result"
#n3=`echo $result|grep "page_id" -c`
#echo "************************************************"

result=`$MYSQL_BIN -h 10.81.50.211 -u video -pvideo video -e "select *,from_unixtime(crt_time) from normal_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "normal_url is:
#$result"
#n4=`echo $result|grep "page_id" -c`
#echo "************************************************"

result=`$MYSQL_BIN -h 10.81.50.211 -u video -pvideo video -e "select *,from_unixtime(crt_time) from sobar_url${index} where
 link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "sobar_url is:
#$result" 

#n5=`echo $result|grep "page_id" -c`

n5=`echo $result|grep "crt_time"|awk -F "):" '{print $2}'`
echo -e  $1"\t"$n1"\t"$n2"\t"$n3"\t"$n4"\t"$n5


exit 0
