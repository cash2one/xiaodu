#!/bin/bash

source conf/db_mis.conf
urls=./data/urls
urls_manul=./data/urls_manul

#load url from db
${mysql} -h${db_host} -P${db_port} -u${db_user} -p${db_pwd} ${db_name} -NB -e "select url from localch_list where block_sign like '2_%';" > $urls
echo "get urls from localch_list by 2:[`wc -l $urls`]"
${mysql} -h${db_host} -P${db_port} -u${db_user} -p${db_pwd} ${db_name} -NB -e "select url from localch_index where block_sign like '2_%' and weight<100;" >> $urls
echo "get urls from localch_index by 2:[`wc -l $urls`]"
grep -v "v.baidu.com" $urls > data/tmp
mv data/tmp $urls
echo "filte the v.baidu.com urls:[`wc -l $urls`]"
cat $urls_manul >> $urls
echo "add the urls_manul to urls:[`wc -l $urls`]"

#download url and then parse the content
cnt=1
while read url
do
	cnt=`expr $cnt + 1`
	pid=`echo $url | md5sum | awk '{print $1}'`
	if [ -s page/${pid}.html ] && [ -s ./results/${pid} ];then
		echo "dup task. skip!"
		continue
	fi
	wget -q -O page/${pid}.html "$url"
	if [ $? -eq 0 ];then
		python parser.py "$url" "./page/${pid}.html" "$pid"
		#save the result to db
		if [ $? -eq 0 ];then
			~/php/bin/php pushdatatodb.php ./results/${pid} >> log/pushdatatodb.log
		else
			echo "parse failed! push nothing to db. url:$url"
		fi
		echo "process url at[$cnt] SUC"
	else
		echo "wget url failed at[$cnt] url:$url"
	fi
	sleep 1
done<$urls

