#!/bin/bash

source ./conf/db.conf

files_need_convert=./data/baipinghui_file_need_convert_id_reallink_format
convert_log=./log/baipinghui_convert.log

#get all links need convert
${mysql} -h${db_host} -P${db_port} -u${db_user} -p${db_pwd} ${db_name} -NB -e " select id, \"3083\" as format, bcs_url from tbl_video_ori_mis where v_status <= 1 and bcs_url != \"\" and bcs_url_compress_high = \"\";  " > ${files_need_convert}
if [ $? -ne 0 ]
then
	echo "get url need conver failed!"
	exit 1
fi
echo "get url need converted [`wc -l ${files_need_convert}`]"

#start convert
python baipinghui_convert.py $files_need_convert >> $convert_log
if [ $? -ne 0 ];then
	echo "send convert failed!"
fi
echo "send convert all success!"

#push data into baishi
echo "begin pushdata2baishi" >> $convert_log
~/odp/php/bin/php baipinghui_pushdata2baishi.php >> $convert_log
