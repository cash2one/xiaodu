#!/bin/sh

PAGENUM=`grep 'page_table_num' /home/video/indexdb/conf/indexdb.conf|awk -F ":" '{print $2}'|awk '{print $1}'`
RESULT=/home/video/indexdb/data/send/deadlinktemp.txt
OUTPUT=/home/video/indexdb/data/send/deadlink.txt
LOGFILE=/home/video/indexdb/log/japan_getdeadlink.log

echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "start running $0" >>$LOGFILE
echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "starttime=$STARTTIME,pagenum=$PAGENUM" >>$LOGFILE

STARTTIME=`date -d '22 day ago' +%s`

>$RESULT

for((i=1;i<=$PAGENUM;i++))
do
	echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "new select form page$i" >>$LOGFILE
	/home/video/database/mysql/bin/mysql -uroot video -e "select link from spider_url$i where dead_check_time>$STARTTIME and flag_dead=2" | awk '{if(NR>1)print $0}' >> $RESULT
	ret=$?
	if [ $ret -ne 0 ]
	then
		echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "select form page$i failed, errcode=$ret" >>$LOGFILE
	fi

	echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "new select form given_page$i" >>$LOGFILE
	/home/video/database/mysql/bin/mysql -uroot video -e "select link from videomap_url$i where dead_check_time>$STARTTIME and flag_dead=2" | awk '{if(NR>1)print $0}' >> $RESULT
	ret=$?
	if [ $ret -ne 0 ]
	then
		echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "select form given_page$i failed, errcode=$ret" >>$LOGFILE
	fi
done

awk '++num[$0]==1{print $0}'  $RESULT > $OUTPUT

echo "[`date "+%Y-%m-%d %H:%M:%S"`]" "this shell running finished!" >>$LOGFILE

exit 0

