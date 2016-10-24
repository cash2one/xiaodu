#!/bin/bash
#set -x

cd /home/rd/
if [ $# -ne 1 ]
then

	echo "./url_page_index.sh url"
	exit 
fi
url=`echo "$1" | awk '{print $0}'`
#echo "$url"
#exit 0

sign1=`./print_sign "$url" | awk '{print $1}'`
sign1=`echo $sign1`

sign2=`./print_sign "$url" | awk '{print $2}'`
sign2=`echo $sign2`

sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`


echo "sign1 is :"$sign1
echo "sign2 is :"$sign2
echo $index

result=`~/mysql -u root video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`

echo "our result is:
$result"

echo "************************************************"

result=`~/mysql -u root video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`

echo "vm result is:
$result"

echo "************************************************"
