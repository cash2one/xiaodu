#!/bin/bash
set -x

cd /home/rd/
while read line
do
sign1=`echo $line | awk '{print $1}'`
sign2=`echo $line | awk '{print $2}'`

sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`
MYSQL_PATH=/home/video/database/mysql/


MYSQL_CMD="select link,link_sign1,link_sign2,duration from spider_url"$index" where link_sign1=$sign1 and link_sign2=$sign2 "
if(($index%2==0))
then
	$MYSQL_PATH/bin/mysql -h "10.26.26.87" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
else
	$MYSQL_PATH/bin/mysql -h "10.36.4.241" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
fi

MYSQL_CMD="select link,link_sign1,link_sign2,duration from videomap_url"$index" where link_sign1=$sign1 and link_sign2=$sign2 "
if(($index%2==0))
then
        $MYSQL_PATH/bin/mysql -h "10.26.26.87" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
else
        $MYSQL_PATH/bin/mysql -h "10.36.4.241" -P 6141 -uvideo_daku_w -p19DjslUyNs09 -e "$MYSQL_CMD" | grep http >> $2
fi
done<$1
exit 0
