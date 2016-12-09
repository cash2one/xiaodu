#!/bin/bash

source ./conf/db.conf

${mysql} -h${db_host} -P${db_port} -u${db_user} -p${db_pwd} ${db_name} -NB < sqls/sql_dump_links_2_yulei.sql > data/tmp
echo "begin[`date`] raw data:[`wc -l data/tmp`]"

mv data/allplaylink_baidulink_aipai data/allplaylink_baidulink_aipai_`date '-d 1 days ago' +%Y%m%d`
grep "aipai.com" data/tmp | awk -F'\t' '{if($3==0){print $1"\t"$2}}' > data/allplaylink_baidulink_aipai
grep "www.letv.com" data/tmp | awk -F'\t' '{if($3==0){print $1"\t"$2}}' | sed 's/baishi.baidu.com/baidu.hz.letv.com/g' >> data/allplaylink_baidulink_aipai
grep ".ku6.com/" data/tmp | awk -F'\t' '{if($3==0){print $1"\t"$2}}' | sed 's/baishi.baidu.com/baidu.ku6.com/g' >> data/allplaylink_baidulink_aipai
grep ".baomihua.com/" data/tmp | awk -F'\t' '{if($3==0){print $1"\t"$2}}' | sed 's/baishi.baidu.com/baidu.baomihua.com/g' >> data/allplaylink_baidulink_aipai
echo "end[`date`] after filter [`wc -l data/allplaylink_baidulink_aipai`]"
