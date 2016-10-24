#!/bin/bash
#set -x


MYSQL_BIN=/home/video/database/mysql/bin/mysql
url="$1";

#echo "$url";

echo "内嵌url: $url";
echo "内嵌数据库情况请翻到页底部";
id=`echo "$url" | sed 's/.html.*//' | sed 's#.*/##' `
#echo $id;
table_name=`python /home/video/q_url/neiqian/gettablename.py $id`
#echo $table_name;

url=""
if [ ${#table_name} -gt 0 ]
then
	url=`$MYSQL_BIN -h 10.42.8.95 -P6145 -u video_yingshi_yu -pqmyOzEPruA1K video_yingshi --skip-column-names -e "select play_link from tbl_video_${table_name} where play_link_sign64='$id'"`
	#echo "原始url: $url";
	sh /home/video/q_url/url_page_index.sh $url
	
	url=`$MYSQL_BIN -h 10.42.8.95 -P6145 -u video_yingshi_yu -pqmyOzEPruA1K video_yingshi -e "select * from tbl_video_${table_name} where play_link_sign64='$id' \G"`
fi


#内嵌库数据情况
echo "内嵌库数据情况";
echo "$url";
exit;

sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`

MYSQL_BIN=/home/video/database/mysql/bin/mysql
echo "sign1 is :"$sign1
echo "sign2 is :"$sign2
echo $index
if((`expr $index % 2` == 0))
then
cmd="$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e \"select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G\""
result=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
else
cmd="$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e \"select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G\""
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
fi

echo $cmd
echo
echo "spider_url is:
$result"

echo "************************************************"

if((`expr $index % 2` == 0))
then
result=`$MYSQL_BIN -h 10.26.26.87 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
else
result=`$MYSQL_BIN -h 10.36.4.241 -P 6141 -u video_daku_r -phH6qHmN6ZCGW video -e "select *,from_unixtime(crt_time),from_unixtime(dist_date),from_unixtime(dead_check_time) from videomap_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
fi
echo "videomap_url is:
$result"


echo "************************************************"

#result=`$MYSQL_BIN -h 10.26.26.87 -P4200 -uvideo_w -pNs09NHJL video -e "select *,from_unixtime(crt_time) from possible_url${index} where link_sign3=$sign1 and link_sign2=$sign2\G"`
#echo "possible_url is:
#$result"

#echo "************************************************"

#result=`$MYSQL_BIN -h 10.26.26.87 -P4200 -uvideo_w -pNs09NHJL video -e "select *,from_unixtime(crt_time) from normal_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "normal_url is:
#$result"

#echo "************************************************"

#result=`$MYSQL_BIN -h 10.81.50.211 -u video -pvideo video -e "select *,from_unixtime(crt_time) from sobar_url${index} where
#result=`$MYSQL_BIN -h 10.26.26.87 -u video -pvideo video -e "select *,from_unixtime(crt_time) from sobar_url${index} where
# link_sign1=$sign1 and link_sign2=$sign2\G"`
#echo "sobar_url is:
#$result" 
exit 0
