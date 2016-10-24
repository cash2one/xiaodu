#!/bin/bash

#定时为news导出新闻视频

set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
MAILLIST=$(head -n 1 ../share/mail.conf)
MAILLIST=wangweixin@baidu.com

#得到title_metadata表的数目
CONF_NAME=indexdb.conf
CONF_PATH=../conf/
page_table_num=`grep 'page_table_num' ${CONF_PATH}${CONF_NAME} | awk -F ":" '{print $2}'`
page_table_num=64
STARTTIME=`date -d '4 days ago 00:00:00' +%s`
STARTTIME=`date -d '1 days ago' +%s`

DESTDATAPATH=/home/rd
DESTDATAFILE=${DESTDATAPATH}/newsvideo/`date +%y%m%d%H`.txt
MYSQL_BIN=/home/video/database/mysql/bin/mysql

> "${DESTDATAFILE}.tmp"

page_table_num=8 

for((i=1;i<=$page_table_num;i++))
do
	date "+[%y-%m-%d %H:%M:%S]"
	${MYSQL_BIN} -uroot video -e "select link,image_sign1,image_sign2,page_title,anchor,'' from spider_url"${i}" where crt_time>"$STARTTIME" and hot_flag=2 and flag_dead=0" | awk 'NR>1{print $0}' >> "${DESTDATAFILE}.tmp"
	if [ $? -ne 0 ]
	then
		echo "select normal_info for news failed!" | mail -s "[select normal_info for news][VIDEO][${host}][${today}]" ${MAILLIST}
		exit 1
	fi
done

line=`wc -l ${DESTDATAFILE}.tmp | awk '{print $1}'`
if [ $line -eq 0 ]
then
	echo "select data for news file is null!" | mail -s "[select normal_info for news][${host}][${today}]" ${MAILLIST}
	exit 1
fi

mv "${DESTDATAFILE}.tmp" "${DESTDATAFILE}"

date "+[%y-%m-%d %H:%M:%S]"

exit 0

