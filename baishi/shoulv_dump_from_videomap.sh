#!/bin/bash

#data_videomap_path="ftp://db-video-lc01.db01.baidu.com//home/video/shiym/dump_for_baiduyingshi/data/data_all_dump"
data_videomap_path="ftp://nj02-video-aldmine02.nj02.baidu.com//home/video/shiym/data/data_all_dump"
data_videomap=./data/data_from_videomap
data_sql_videomap=./data/sql_from_videomap

rm -f $data_videomap
wget -O ${data_videomap} ${data_videomap_path}
if [ $? -ne 0 ];then
	echo "wget data_videomap failed! path:[$data_videomap_path]"
	exit 1
fi
echo "wget data ok at[`date`] info:[`wc -l ${data_videomap}`]"

#generate sql
mv ${data_sql_videomap} ${data_sql_videomap}_`date +%Y%m%d`
~/php/bin/php shoulv_dump_from_videomap.php > log/dump_from_videomap_`date +%Y%m%d`.log 2>&1
if [ $? -ne 0 ];then
	echo "insert into database failed!"
	exit 1
fi

echo "insert dump data OK!"
