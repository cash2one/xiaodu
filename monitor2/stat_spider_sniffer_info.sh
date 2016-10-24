#!/bin/bash
set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
MAILLIST=$(head -n 1 ../share/mail.conf)
#MAILLIST="video-rd@baidu.com video-pm@baidu.com"
#MAILLIST="caochunliang@baidu.com"
MAILLIST="tanguoqiang@baidu.com"
MYSQL_PATH=/home/video/database/mysql/
formal_num_file=./spider_sniffer_num.txt

export LANG=zh_CN.GBK

spider_succ_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from spider_url1 where link_status=3" | awk 'NR>1{print $0}'`
spider_succ_link=`echo $spider_succ_link`

spider_flv_succ_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from spider_url1 where link_status=1" | awk 'NR>1{print $0}'`
spider_flv_succ_link=`echo $spider_flv_succ_link`

spider_flv_fail_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from spider_url1 where link_status=-1" | awk 'NR>1{print $0}'`
spider_flv_fail_link=`echo $spider_flv_fail_link`

spider_fail_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from spider_url1 where link_status=-3" | awk 'NR>1{print $0}'`
spider_fail_link=`echo $spider_fail_link`

spider_get_link_fail=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from spider_url1 where link_status=-2" | awk 'NR>1{print $0}'`
spider_get_link_fail=`echo $spider_get_link_fail`


videomap_succ_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from videomap_url1 where link_status=3" | awk 'NR>1{print $0}'`
videomap_succ_link=`echo $videomap_succ_link`

videomap_flv_succ_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from videomap_url1 where link_status=1" | awk 'NR>1{print $0}'`
videomap_flv_succ_link=`echo $videomap_flv_succ_link`

videomap_flv_fail_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from videomap_url1 where link_status=-1" | awk 'NR>1{print $0}'`
videomap_flv_fail_link=`echo $videomap_flv_fail_link`

videomap_fail_link=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from videomap_url1 where link_status=-3" | awk 'NR>1{print $0}'`
videomap_fail_link=`echo $videomap_fail_link`

videomap_get_link_fail=`${MYSQL_PATH}bin/mysql -u root video -e "select count(*) from videomap_url1 where link_status=-2" | awk 'NR>1{print $0}'`
videomap_get_link_fail=`echo $videomap_get_link_fail`

spider_succ_link=`expr $spider_succ_link \* 128`
spider_flv_succ_link=`expr $spider_flv_succ_link \* 128`
spider_flv_fail_link=`expr $spider_flv_fail_link \* 128`
spider_fail_link=`expr $spider_fail_link \* 128`
spider_get_link_fail=`expr $spider_get_link_fail \* 128`

videomap_succ_link=`expr $videomap_succ_link \* 128`
videomap_flv_succ_link=`expr $videomap_flv_succ_link \* 128`
videomap_flv_fail_link=`expr $videomap_flv_fail_link \* 128`
videomap_fail_link=`expr $videomap_fail_link \* 128`
videomap_get_link_fail=`expr $videomap_get_link_fail \* 128`

last_spider_succ_link=0
last_spider_flv_succ_link=0
last_spider_flv_fail_link=0
last_spider_fail_link=0
last_spider_get_link_fail=0

last_videomap_succ_link=0
last_videomap_flv_succ_link=0
last_videomap_flv_fail_link=0
last_videomap_fail_link=0
last_videomap_get_link_fail=0

j=0
while read i
do
	j=`expr $j + 1`
	
	case $j in
	1)
		last_spider_succ_link=$i
	;;
	2)
	 	last_spider_flv_succ_link=$i
	;;
	3)
		last_spider_flv_fail_link=$i
	;;
	4)
		last_spider_fail_link=$i
	;;
	5)	
		last_spider_get_link_fail=$i
	;;
	6)	
		last_videomap_succ_link=$i
	;;
	7)	
		last_videomap_flv_succ_link=$i
	;;
	8)	
		last_videomap_flv_fail_link=$i
	;;
	9)      
		last_videomap_fail_link=$i
        ;;
	10)     
		last_videomap_get_link_fail=$i
        ;;
	esac 

done < $formal_num_file


diff_spider_succ_link=`expr $spider_succ_link - $last_spider_succ_link`
diff_spider_flv_succ_link=`expr $spider_flv_succ_link - $last_spider_flv_succ_link`
diff_spider_flv_fail_link=`expr $spider_flv_fail_link - $last_spider_flv_fail_link`
diff_spider_fail_link=`expr $spider_fail_link - $last_spider_fail_link`
diff_spider_get_link_fail=`expr $spider_get_link_fail - $last_spider_get_link_fail`

diff_videomap_succ_link=`expr $videomap_succ_link - $last_videomap_succ_link`
diff_videomap_flv_succ_link=`expr $videomap_flv_succ_link - $last_videomap_flv_succ_link`
diff_videomap_flv_fail_link=`expr $videomap_flv_fail_link - $last_videomap_flv_fail_link`
diff_videomap_fail_link=`expr $videomap_fail_link - $last_videomap_fail_link`
diff_videomap_get_link_fail=`expr $videomap_get_link_fail - $last_videomap_get_link_fail`

echo $spider_succ_link > $formal_num_file
echo $spider_flv_succ_link >> $formal_num_file
echo $spider_flv_fail_link >> $formal_num_file
echo $spider_fail_link >> $formal_num_file
echo $spider_get_link_fail >> $formal_num_file

echo $videomap_succ_link >> $formal_num_file
echo $videomap_flv_succ_link >> $formal_num_file
echo $videomap_flv_fail_link >> $formal_num_file
echo $videomap_fail_link >> $formal_num_file
echo $videomap_get_link_fail >> $formal_num_file

echo "***********spider通过video-sniffer提链接和提图情况****************
成功提链接和提图情况:总量$spider_succ_link条,新增:$diff_spider_succ_link条
成功提链接情况:总量$spider_flv_succ_link条,新增:$diff_spider_flv_succ_link条
提链接失败:总量$spider_flv_fail_link条,新增:$diff_spider_flv_fail_link条
下载失败:总量$spider_get_link_fail条,新增:$diff_spider_get_link_fail条
提图失败:总量$spider_fail_link条,新增:$diff_spider_fail_link条" > mail_tmp.txt

echo "***********videomap通过video-sniffer提链接和提图情况****************
成功提链接和提图情况:总量$videomap_succ_link条,新增:$diff_videomap_succ_link条
成功提链接情况:总量$videomap_flv_succ_link条,新增:$diff_videomap_flv_succ_link条
提链接失败:总量$videomap_flv_fail_link条,新增:$diff_videomap_flv_fail_link条
下载失败:总量$videomap_get_link_fail条,新增:$diff_videomap_get_link_fail条
提图失败:总量$videomap_fail_link条,新增:$diff_videomap_fail_link条" >> mail_tmp.txt


cat mail_tmp.txt | mutt -s "[统计][P2P][${host}][${today}]P2P数据量统计" ${MAILLIST}

exit 0

