#!/bin/bash
set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
MAILLIST=$(head -n 1 ../share/mail.conf)
#MAILLIST="video-rd@baidu.com video-pm@baidu.com"
#MAILLIST="tanguoqiang"@baidu.com
MYSQL_PATH=/home/p2p/database/mysql/
RAW_PATH=/home/p2p/p2p_index/data/raw/
formal_num_file=../data/formal_link_num.txt
bt_res_file=../data/bt_res.txt
emule_res_file=../data/emule_res.txt
export LANG=zh_CN.GBK
#
bt_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1" | awk 'NR>1{print $0}'`
bt_count=`echo $bt_count`
emule_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(fromurl_sign1)  from emule1" | awk 'NR>1{print $0}'`
emule_count=`echo $emule_count`
all_count=`expr $bt_count + $emule_count`
#
btsite_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(site_id) from bt_site" | awk 'NR>1{print $0}'`
btsite_count=`echo $btsite_count`
emulesite_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(site_id) from emule_site" | awk 'NR>1{print $0}'`
emulesite_count=`echo $emulesite_count`
site_count=`expr $btsite_count + $emulesite_count`
#
bt_res_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select filelist from bt1 where torrentfile_sign1!=0 or torrentfile_sign2!=0" | awk -F "[$]+" 'BEGIN{total=0}{total+=NF}END{total-=NR;print total}'`
emule_res_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select seed_url from emule1 where resources_sign1!=0 or resources_sign2!=0" |awk -F "[$]+" 'BEGIN{total=0}{total+=NF}END{total-=NR;print total}'`

#
bt_succ_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1 where (torrentfile_sign1!=0 or torrentfile_sign2!=0) and flag_dead=0 " | awk 'NR>1{print $0}'`
bt_succ_count=`echo $bt_succ_count`

bt_not_video_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1 where flag_dead=-2 " | awk 'NR>1{print $0}'`
bt_not_video_count=`echo $bt_not_video_count`

bt_not_torrent_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1 where flag_dead=-1 " | awk 'NR>1{print $0}'`
bt_not_torrent_count=`echo $bt_not_torrent_count`

bt_dead_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1 where flag_dead=1 " | awk 'NR>1{print $0}'`
bt_dead_count=`echo $bt_dead_count`

bt_bad_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(link_sign1) from bt1 where torrent_quality!=0 and flag_dead=0 " | awk 'NR>1{print $0}'`
bt_bad_count=`echo $bt_bad_count`

emule_no_res_count=`${MYSQL_PATH}bin/mysql -u root p2p -e "select count(fromurl_sign1) from emule1 where resources_sign1=0 and resources_sign2=0 " | awk 'NR>1{print $0}'`
emule_no_res_count=`echo $emule_no_res_count`

emule_has_res_link=`expr $emule_count - $emule_no_res_count`


last_all_count=0
last_site_count=0
last_bt_count=0
last_emule_count=0
last_emulesite_count=0
last_btsite_count=0
last_bt_res_count=0
last_emule_res_count=0
last_bt_succ_count=0
last_bt_not_video_count=0
last_bt_not_torrent_count=0
last_bt_dead_count=0
last_bt_bad_count=0
last_emule_no_res_count=0

j=0
while read i
do
	j=`expr $j + 1`
	
	case $j in
	1)
		last_all_count=$i
	;;
	2)
	 	last_bt_count=$i
	;;
	3)
		last_emule_count=$i
	;;
	4)
		last_site_count=$i
	;;
	5)
		last_btsite_count=$i
	;;
	6)
		last_emulesite_count=$i
	;;
	7)
		last_bt_res_count=$i
	;;
	8)
		last_emule_res_count=$i
	;;
	9)
		last_bt_succ_count=$i
	;;
	10)
		last_bt_not_video_count=$i
	;;
	11)
		last_bt_not_torrent_count=$i
	;;
	12)
		last_bt_dead_count=$i
	;;
	13)
		last_bt_bad_count=$i
	;;
	14)
		last_emule_no_res_count=$i
	;;
	esac 

done < $formal_num_file

diff_all_count=`expr $all_count - $last_all_count`
diff_bt_count=`expr $bt_count - $last_bt_count`
diff_emule_count=`expr $emule_count - $last_emule_count`
diff_site_count=`expr $site_count - $last_site_count` 
diff_emulesite_count=`expr $emulesite_count - $last_emulesite_count` 
diff_btsite_count=`expr $btsite_count - $last_btsite_count` 
diff_bt_res_count=`expr $bt_res_count - $last_bt_res_count` 
diff_emule_res_count=`expr $emule_res_count - $last_emule_res_count` 
diff_bt_succ_count=`expr $bt_succ_count - $last_bt_succ_count`
diff_bt_not_video_count=`expr $bt_not_video_count - $last_bt_not_video_count`
diff_bt_not_torrent_count=`expr $bt_not_torrent_count - $last_bt_not_torrent_count`
diff_bt_dead_count=`expr $bt_dead_count - $last_bt_dead_count`
diff_bt_bad_count=`expr $bt_bad_count - $last_bt_bad_count`
diff_emule_no_res_count=`expr $emule_no_res_count - $last_emule_no_res_count`

echo $all_count > $formal_num_file
echo $bt_count >> $formal_num_file
echo $emule_count >> $formal_num_file
echo $site_count >> $formal_num_file
echo $btsite_count >> $formal_num_file
echo $emulesite_count >> $formal_num_file
echo $bt_res_count>> $formal_num_file
echo $emule_res_count >> $formal_num_file
echo $bt_succ_count >> $formal_num_file
echo $bt_not_video_count >> $formal_num_file
echo $bt_not_torrent_count >> $formal_num_file
echo $bt_dead_count >> $formal_num_file
echo $bt_bad_count >> $formal_num_file
echo $emule_no_res_count >> $formal_num_file

MUL=64

echo "***********P2P数据总量****************
p2p数据总量: `expr $all_count \* $MUL` 条,新增:`expr $diff_all_count \* $MUL` 条
其中:
bt链接数: `expr $bt_count \* $MUL` 条,新增`expr $diff_bt_count \* $MUL` 条
emule链接数: `expr $emule_count \* $MUL` 条,新增`expr $diff_emule_count \* $MUL` 条
bt资源数: `expr $bt_res_count \* $MUL` 条,新增`expr $diff_bt_res_count \* $MUL` 条
emule资源数:`expr $emule_res_count \* $MUL` 条,新增`expr $diff_emule_res_count \* $MUL` 条" > mail_tmp.txt

echo "***********P2P站点情况****************
站点总数: $site_count ,新增$diff_site_count 
bt站点数: $btsite_count ,新增$diff_btsite_count
emule站点数: $emulesite_count,新增$diff_emulesite_count " >> mail_tmp.txt

echo "***********bt数据情况********
bt成功解析的数据:`expr $bt_succ_count \* $MUL` 条,新增`expr $diff_bt_succ_count \* $MUL` 条
bt非视频种子数:`expr $bt_not_video_count \* $MUL` 条,新增`expr $diff_bt_not_video_count \* $MUL` 条
bt非种子数:`expr $bt_not_torrent_count \* $MUL` 条,新增`expr $diff_bt_not_torrent_count \* $MUL` 条
bt死链数:`expr $bt_dead_count \* $MUL`条,新增`expr $diff_bt_dead_count \* $MUL`条
bt质量不好的链接数:`expr $bt_bad_count \* $MUL`条,新增`expr $diff_bt_bad_count \* $MUL` 条">> mail_tmp.txt

echo "***********emule数据情况********
emule没有资源的链接数:`expr $emule_no_res_count \* $MUL` 条,新增`expr $diff_emule_no_res_count \* $MUL` 条
emule链接平均资源数：`expr $emule_res_count / $emule_has_res_link` ">> mail_tmp.txt


cat mail_tmp.txt | mutt -s "[统计][P2P][${host}][${today}]P2P数据量统计" ${MAILLIST}

exit 0
