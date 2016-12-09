#!/bin/bash

source ./conf/db.conf

#dump tbl_video_xx
for ((i=1;i<=64;i++))
do

	~/mysql/bin/mysqldump -h10.42.8.95 -P6145 -uvideo_yingshi_yu -pqmyOzEPruA1K --complete-insert=true --lock-tables=false --extended-insert=false video_yingshi  tbl_video_${i} -w " site='aipai.com' "  > data/bak_tbl_video_aipai_${i}

done
echo "dump tbl_video_xx SUC!"
