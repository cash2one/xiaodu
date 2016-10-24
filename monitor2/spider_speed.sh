#!/bin/sh

set -x
mysql="/home/video/database/mysql/bin/mysql"

beg_time=`date +%s -d "7 days ago"`

nowday=`date "+%Y%m%d"`


> ./data/videomap.txt
> ./data/spider.txt

for i in 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 
do
	mysql_cmd="select link,crt_time, dist_date from videomap_url$i  where crt_time>dist_date and dist_date > $beg_time"
	$mysql  -h10.23.255.128 -u video -pvideo video --skip-column-names  -e "$mysql_cmd" >> "./data/videomap.txt"

	mysql_cmd="select link,crt_time from spider_url$i  where crt_time> $beg_time"
	$mysql  -h10.23.255.128 -u video -pvideo video --skip-column-names  -e "$mysql_cmd" >> "./data/spider.txt"
done

awk -F '\t' '{if(ARGV[1]==FILENAME){A[$1]=$3;} else{if($1 in A){ split($1, arr, "/"); if($2>A[$1])print arr[3]"\t"($2-A[$1])/3600"\t"$1;}} }' ./data/videomap.txt ./data/spider.txt > ./data/com_link.txt

awk -F '\t' '{if($2<=240){A[$1]+=$2; B[$1]++;}}END{for (i in A){print i"\t"A[i]/B[i]"\t"B[i] }}'  ./data/com_link.txt | sort -nrk3,3 -t'	' > ./data/spider_speed_res.txt


> ./data/big_site.$nowday
> ./data/small_site.$nowday

for i in `cat ./conf/big_site.txt`
do
	awk -F '\t' -v site=$i  '{if( index($1, site) != 0) print $0}' ./data/spider_speed_res.txt >> ./data/big_site.$nowday
done

awk -F '\t' '{if(FILENAME==ARGV[1]) A[$1]=1; else if($1 in A) {} else {print $0} }' ./data/big_site.$nowday ./data/spider_speed_res.txt > ./data/small_site.$nowday

awk -F '\t' '{if($1!="www.tudou.com"){link+=$3; time+=$2*$3}}END{print "big site avg latency:" time/link}' ./data/big_site.$nowday >> ./data/big_site.$nowday
awk -F '\t' '{if($1!="www.tudou.com"){link+=$3; time+=$2*$3}}END{print "small site avg latency:" time/link}' ./data/small_site.$nowday >> ./data/small_site.$nowday

awk -F '\t' '{split($1, arr, "/"); latency=($2-$3)/3600; if(latency <= 240){A[arr[3]]++; B[arr[3]]+=latency;} }END{for (i in A){print i"\t"B[i]/A[i]"\t"A[i]}}' ./data/videomap.txt | sort -nrk3,3 > ./data/videomap_speed.$nowday 

awk -F '\t' '{if($1!="www.tudou.com")link+=$3; time+=$2*$3}END{print "videomap site avg latency:" time/link}' ./data/videomap_speed.$nowday >> ./data/videomap_speed.$nowday


