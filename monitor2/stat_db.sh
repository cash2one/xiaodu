#!/bin/bash
set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
MAILLIST=$(head -n 1 ../share/mail.conf)
#MAILLIST="video-rd@baidu.com video-pm@baidu.com video-op@baidu.com"
MAILLIST="tanguoqiang@baidu.com"
#MAILLIST="wangweixin@baidu.com"
MYSQL_PATH=/home/video/database/mysql/
RAW_PATH=/home/video/video_index/data/raw/
formal_num_file=./normal_link_num.txt
site_file=/home/video/indexdb/data/send/fs_site.txt

export LANG=zh_CN.GBK

our_link=`${MYSQL_PATH}bin/mysql -u root video -e "select sum(page_num) from spider_site" | awk 'NR>1{print $0}'`
our_link=`echo $our_link`
vm_link=`${MYSQL_PATH}bin/mysql -u root video -e "select sum(page_num) from videomap_site" | awk 'NR>1{print $0}'`
vm_link=`echo $vm_link`
normal_link_num=`awk -F "\t" 'BEGIN{count=0;mms_count=0;rtsp_count=0;http_count=0}$3==""{next}{count++}{IGNORECASE=1;if($3~/^mms/){mms_count++;next};if($3~/^rtsp/){rtsp_count++;next};if($3~/^http/){http_count++;next};}END{print count"\t"mms_count"\t"rtsp_count"\t"http_count}' ${RAW_PATH}raw.[0-9] ${RAW_PATH}raw.[1-2][0-9] ${RAW_PATH}raw.3[0-1]`
all_count=`echo $normal_link_num | awk '{print $1}'`
mms_count=`echo $normal_link_num | awk '{print $2}'`
rtsp_count=`echo $normal_link_num | awk '{print $3}'`
http_count=`echo $normal_link_num | awk '{print $4}'`

#2层库，数量乘2
all_count=`expr $all_count + $all_count`
mms_count=`expr $mms_count + $mms_count`
rtsp_count=`expr $rtsp_count + $rtsp_count`
http_count=`expr $http_count + $http_count`

site_count=`awk '++num[$2]==1{total++}END{print total}' ${RAW_PATH}/raw.0  ${RAW_PATH}/raw.*.normal`

last_all_count=0
lastmms_count=0
last_rtsp_count=0
last_http_count=0
last_site_count=0
last_our_link=0
last_vm_link=0
last_indexdb_all_link=0

j=0
while read i
do
	j=`expr $j + 1`
	
	case $j in
	1)
		last_all_count=$i
	;;
	2)
	 	last_mms_count=$i
	;;
	3)
		last_rtsp_count=$i
	;;
	4)
		last_http_count=$i
	;;
	5)	last_site_count=$i
	;;
	6)	last_our_link=$i
	;;
	7)	last_vm_link=$i
	;;
	8)	last_indexdb_all_link=$i
	;;
	esac 

done < $formal_num_file


#fi
#统计站点的数据信息
 #先统计自己抓取的站点信息
${MYSQL_PATH}bin/mysql -u root video -e "select site,page_num from spider_site order by page_num desc" | awk 'NR>1{print $0}' > site_stat.new

awk -F "\t" 'FILENAME=="site_stat.new"{a[$1]=$2;c[$1]=$2;next}{c[$1]=a[$1]-$2;next}END{for(x in c)print x"\t"a[x]"\t"c[x]}' site_stat.new site_stat.old | sort -t '	' -k3,3 -nr | awk -F "\t" '$3>50{printf("%-20s%-20d%-20d\n",$1,$2,$3)}'> site_add.txt

mv site_stat.new site_stat.old

 #再统计videomap的站点信息
${MYSQL_PATH}bin/mysql -u root video -e "select site,page_num from videomap_site order by page_num desc" | awk 'NR>1{print $0}' > vm_site_stat.new

awk -F "\t" 'FILENAME=="vm_site_stat.new"{a[$1]=$2;c[$1]=$2;next}{c[$1]=a[$1]-$2}END{for(x in c)print x"\t"a[x]"\t"c[x]}' vm_site_stat.new vm_site_stat.old | sort -t '	' -k3,3 -nr | awk -F "\t" '$3>0{printf("%-20s%-20d%-20d\n",$1,$2,$3)}'> vm_site_add.txt

mv vm_site_stat.new vm_site_stat.old

#新增加的报表内容

>mail_tmp.txt
>mail_ahead.txt

PAGENAME=spider_url
PAGENUM=28

OUR_TotalDataNum=0
OUR_NO_IMGLINK_NUM=0
OUR_NO_IMAGE_NUM=0
OUR_NO_PLAYTITLE_NUM=0
OUR_NO_TAG_NUM=0
OUR_NO_COMMENT=0
OUR_NO_DISTDATE=0
OUR_NO_DURATION=0
OUR_NO_IMGLINK_PRO_FAIL_NUM=0
OUR_NO_IMGLINK_PRO_SUCC_NUM=0

for((i=28;i<=$PAGENUM;i++))
do
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(page_id) from $PAGENAME$i where flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_TotalDataNum=`expr $OUR_TotalDataNum + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(image_link_sign1) from $PAGENAME$i where image_link_sign1=0 and image_link_sign2=0 and flag_dead=0" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_NUM=`expr $OUR_NO_IMGLINK_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(link) from $PAGENAME2 where  flag_dead=0 and link_status!=0 and link_status!=3" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_PRO_FAIL_NUM=`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(link) from $PAGENAME2 where flag_dead=0 and link_status=3" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_PRO_SUCC_NUM=`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(image_sign1) from $PAGENAME$i where image_sign1=0 and image_sign2=0 and flag_dead=0" | awk 'NR==2{print $0}'`
        OUR_NO_IMAGE_NUM=`expr $OUR_NO_IMAGE_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(player_title) from $PAGENAME$i where player_title='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_PLAYTITLE_NUM=`expr $OUR_NO_PLAYTITLE_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(tag) from $PAGENAME$i where tag='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_TAG_NUM=`expr $OUR_NO_TAG_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(page_comment) from $PAGENAME$i where page_comment='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_COMMENT=`expr $OUR_NO_COMMENT + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(dist_date) from $PAGENAME$i where dist_date=0 and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_DISTDATE=`expr $OUR_NO_DISTDATE + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(duration) from $PAGENAME$i where duration=0 and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_DURATION=`expr $OUR_NO_DURATION + $TMPNUM`
done

MUL=64
echo "*********************************************************">>mail_tmp.txt
echo "定向抓取 数据情况">>mail_tmp.txt
echo "数据总量" `expr $OUR_TotalDataNum \* $MUL` "条" >>mail_tmp.txt
echo "没有缩略图link的数据量 "`expr $OUR_NO_IMGLINK_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "被video-sniffer处理过提图失败数据量"`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM  \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "被video-sniffer处理过提图成功数据量 "`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM  \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有缩略图签名的数据量 "`expr $OUR_NO_IMAGE_NUM \* $MUL`" ("`expr $OUR_NO_IMAGE_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有play_title的数据量 "`expr $OUR_NO_PLAYTITLE_NUM \* $MUL`" ("`expr $OUR_NO_PLAYTITLE_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有tag       的数据量 "`expr $OUR_NO_TAG_NUM \* $MUL`" ("`expr $OUR_NO_TAG_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有comment   的数据量 "`expr $OUR_NO_COMMENT \* $MUL`" ("`expr $OUR_NO_COMMENT \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有发布时间  的数据量 "`expr $OUR_NO_DISTDATE \* $MUL`" ("`expr $OUR_NO_DISTDATE \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有时长      的数据量 "`expr $OUR_NO_DURATION \* $MUL`" ("`expr $OUR_NO_DURATION \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt

our_link=`expr $OUR_TotalDataNum \* $MUL`


PAGENAME=videomap_url
PAGENUM=28

OUR_TotalDataNum=0
OUR_NO_IMGLINK_NUM=0
OUR_NO_IMAGE_NUM=0
OUR_NO_PLAYTITLE_NUM=0
OUR_NO_TAG_NUM=0
OUR_NO_COMMENT=0
OUR_NO_DISTDATE=0
OUR_NO_DURATION=0
OUR_NO_IMGLINK_PRO_FAIL_NUM=0
OUR_NO_IMGLINK_PRO_SUCC_NUM=0

for((i=28;i<=$PAGENUM;i++))
do
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(page_id) from $PAGENAME$i where flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_TotalDataNum=`expr $OUR_TotalDataNum + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(image_link_sign1) from $PAGENAME$i where image_link_sign1=0 and image_link_sign2=0 and flag_dead=0" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_NUM=`expr $OUR_NO_IMGLINK_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(link) from $PAGENAME2 where  flag_dead=0 and link_status!=0 and link_status!=3" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_PRO_FAIL_NUM=`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(link) from $PAGENAME2 where flag_dead=0 and link_status=3" | awk 'NR==2{print $0}';`
	OUR_NO_IMGLINK_PRO_SUCC_NUM=`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(image_sign1) from $PAGENAME$i where image_sign1=0 and image_sign2=0 and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_IMAGE_NUM=`expr $OUR_NO_IMAGE_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(player_title) from $PAGENAME$i where player_title='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_PLAYTITLE_NUM=`expr $OUR_NO_PLAYTITLE_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(tag) from $PAGENAME$i where tag='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_TAG_NUM=`expr $OUR_NO_TAG_NUM + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(page_comment) from $PAGENAME$i where page_comment='' and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_COMMENT=`expr $OUR_NO_COMMENT + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(dist_date) from $PAGENAME$i where dist_date=0 and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_DISTDATE=`expr $OUR_NO_DISTDATE + $TMPNUM`
	TMPNUM=`${MYSQL_PATH}bin/mysql -uroot video -e "select count(duration) from $PAGENAME$i where duration=0 and flag_dead=0" | awk 'NR==2{print $0}'`
	OUR_NO_DURATION=`expr $OUR_NO_DURATION + $TMPNUM`
done

MUL=64

echo "videomap 数据情况">>mail_tmp.txt
echo "数据总量" `expr $OUR_TotalDataNum \* $MUL` "条">>mail_tmp.txt
echo "没有缩略图link的数据量 "`expr $OUR_NO_IMGLINK_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "被video-sniffer处理过提图失败数据量"`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_PRO_FAIL_NUM  \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "被video-sniffer处理过提图成功数据量 "`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM \* $MUL`" ("`expr $OUR_NO_IMGLINK_PRO_SUCC_NUM  \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有缩略图签名的数据量 "`expr $OUR_NO_IMAGE_NUM \* $MUL`" ("`expr $OUR_NO_IMAGE_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有play_title的数据量 "`expr $OUR_NO_PLAYTITLE_NUM \* $MUL`" ("`expr $OUR_NO_PLAYTITLE_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有tag       的数据量 "`expr $OUR_NO_TAG_NUM \* $MUL`" ("`expr $OUR_NO_TAG_NUM \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有comment   的数据量 "`expr $OUR_NO_COMMENT \* $MUL`" ("`expr $OUR_NO_COMMENT \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有发布时间  的数据量 "`expr $OUR_NO_DISTDATE \* $MUL`" ("`expr $OUR_NO_DISTDATE \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt
echo "没有时长      的数据量 "`expr $OUR_NO_DURATION \* $MUL`" ("`expr $OUR_NO_DURATION \* 100 / $OUR_TotalDataNum`"%)">>mail_tmp.txt

vm_link=`expr $OUR_TotalDataNum \* $MUL`

/home/video/indexdb/shell/stat.raw.awk ~/video_index/conf/filtsite.txt ${RAW_PATH}raw.0 >>mail_tmp.txt
indexdb_all_link=`grep "总共导出给检索端的数据:" mail_tmp.txt |awk -F ":" '{print $2}'`

diff_all_count=`expr $all_count - $last_all_count`
diff_mms_count=`expr $mms_count - $last_mms_count`
diff_rtsp_count=`expr $rtsp_count - $last_rtsp_count`
diff_http_count=`expr $http_count - $last_http_count` 
diff_site_count=`expr $site_count - $last_site_count`
diff_our_link=`expr $our_link - $last_our_link`
diff_vm_link=`expr $vm_link - $last_vm_link`
diff_indexdb_all_link=`expr $indexdb_all_link - $last_indexdb_all_link`
echo $all_count > $formal_num_file
echo $mms_count >> $formal_num_file
echo $rtsp_count >> $formal_num_file
echo $http_count >> $formal_num_file
echo $site_count >> $formal_num_file
echo $our_link >> $formal_num_file
echo $vm_link >> $formal_num_file
echo $indexdb_all_link >> $formal_num_file

echo "共有传统视频: $all_count 条,新增:$diff_all_count 条
其中:
http类型共有: $http_count 条,新增$diff_http_count 条
mms类型共有: $mms_count 条,新增$diff_mms_count 条
rtsp类型共有: $rtsp_count 条,新增$diff_rtsp_count 条

所有线上数据共有站点: $site_count 个,新增$diff_site_count 个
indexdb中:
所有导出链接一共有$indexdb_all_link 个,新增$diff_indexdb_all_link 个
自己共抓取数据$our_link 条,新增$diff_our_link 个
videomap数据共$vm_link 条,新增$diff_vm_link个"  >> mail_ahead.txt

echo "********************************" >> mail_ahead.txt
echo "自己抓取的数据中，变化量最大的前10个站点为:" >> mail_ahead.txt
printf "%-20s%-20s%-20s\n" 站点名 数据总量 增加量 >> mail_ahead.txt

head -10 site_add.txt >> mail_ahead.txt

echo "********************************" >> mail_ahead.txt
echo "videomap抓取的数据中，变化量最大的前10个站点为:" >> mail_ahead.txt
printf "%-20s%-20s%-20s\n" 站点名 数据总量 增加量 >> mail_ahead.txt

head -10 vm_site_add.txt >> mail_ahead.txt

cat mail_ahead.txt mail_tmp.txt | mutt -s "[统计][VIDEO][${host}][${today}]线上数据量统计" -a site_add.txt -a vm_site_add.txt ${MAILLIST}

exit 0

