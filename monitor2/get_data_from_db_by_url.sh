#!/bin/bash
set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
DATE=`date | awk '{print $2"-"$3}'`

MYSQL_PATH=/home/video/database/mysql/
>$2
while read line
do
#	sign1=`echo $line | awk '{print $2}'`
#	sign1=`echo $sign1`
#	sign2=`echo $line | awk '{print $3}'`
#       sign2=`echo $sign2`
	url=`echo $line | awk '{print $1}'`
	sign1=`/home/rd/print_sign $url | awk '{print $1}'`
	sign1=`echo $sign1`

	#sign2=`/print_sign $1 | awk 'NR==3{split($0,a,":");print a[2]}'`
	sign2=`/home/rd/print_sign $url | awk '{print $2}'`
	sign2=`echo $sign2`	
	page_no=`expr $sign1 + $sign2`
	page_no=`expr $page_no % 64`
	page_no=`expr $page_no + 1`
	MYSQL_PATH=/home/video/database/mysql/

	TABLE_INDEX=$page_no

	MYSQL_CMD="select link,from_unixtime(crt_time),from_unixtime(dist_date),duration from spider_url"${TABLE_INDEX}" where link_sign1=$sign1 and link_sign2=$sign2 "
	if(($page_no%2==0))
	then
	$MYSQL_PATH/bin/mysql -h "10.26.26.87" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
	else
	$MYSQL_PATH/bin/mysql -h "10.36.4.241" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
	fi
	
	MYSQL_CMD="select link,from_unixtime(crt_time),from_unixtime(dist_date),duration from videomap_url"${TABLE_INDEX}" where link_sign1=$sign1 and link_sign2=$sign2 "
	if(($page_no%2==0))
	then
	$MYSQL_PATH/bin/mysql -h "10.26.26.87" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
	else
	$MYSQL_PATH/bin/mysql -h "10.36.4.241" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
	fi
done<$1
exit 0
