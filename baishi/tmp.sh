#!/bin/bash

>$2
while read line
do
	title=`echo $line | awk '{print $1}'`
	cid=`echo $line | awk '{print $NF}'`
	url=`grep "$cid" data/urls_baidujiaoyu`
	echo "$line	$url" >> $2
done<$1

exit 0
rm log/tmplog_*
~/odp/php/bin/php shoulv_start.php "jiaoyu.baidu.com" >> log/tmplog_shoulvstart.log
~/odp/php/bin/php tmp_update_duration_byfile.php data/data_duration_baidujiaoyu_all >> log/tmplog_updateduration.log
~/odp/php/bin/php tmp_update_swf_byfile.php data/data_baidujiaoyu_url_swf  >> log/tmplog_updateswf.log
~/odp/php/bin/php tmp_update_category_byfile.php  data/data_baidujiaoyu_url_category123  >> log/tmplog_updatecategory
