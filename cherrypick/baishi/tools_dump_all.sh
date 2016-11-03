#!/bin/bash

source ./conf/db.conf

mkdir -p data/bak_all_`date +%Y%m%d`

#dump tbl_video_xx
for ((i=1;i<=64;i++))
do

	~/mysql/bin/mysqldump -h10.42.8.95 -P6145 -uvideo_yingshi_yu -pqmyOzEPruA1K --complete-insert=true --lock-tables=false --extended-insert=false video_yingshi  tbl_video_${i}  > data/bak_tbl_video_${i}

done
echo "dump tbl_video_xx SUC!"

#dump tbl_album_urlsign tbl_tag_urlsign
~/mysql/bin/mysqldump -h10.42.8.95 -P6145 -uvideo_yingshi_yu -pqmyOzEPruA1K --complete-insert=true --lock-tables=false --extended-insert=false video_yingshi tbl_album_urlsign > data/bak_tbl_album_urlsign
~/mysql/bin/mysqldump -h10.42.8.95 -P6145 -uvideo_yingshi_yu -pqmyOzEPruA1K --complete-insert=true --lock-tables=false --extended-insert=false video_yingshi tbl_tag_urlsign > data/bak_tbl_tag_urlsign

mkdir -p data/bak_all_`date +%Y%m%d`
mv data_bak_tbl_*  data/bak_all_`date +%Y%m%d`
