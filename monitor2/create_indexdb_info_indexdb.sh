#!/bin/bash
#每天为图片抓取进程选取图片的url
set -x
host=`hostname | awk -F "\.baidu\.com" '{print $1}'`
today=`date +%Y%m%d`
MAILLIST=$(head -n 1 ../share/mail.conf)
#MAILLIST="caochunliang@baidu.com"
DATE=`date | awk '{print $2"-"$3}'`
NORMAL_RAW_SERVER=`head -n 1 ../share/normal_raw_server.txt`


#得到title_metadata表的数目
CONF_NAME=indexdb.conf
CONF_PATH=../conf/
page_table_num=`grep 'page_table_num' ${CONF_PATH}${CONF_NAME} | awk -F ":" '{print $2}'`
page_table_num=`echo $page_table_num`

#得到bd的层数以及本机器建的库属于哪一层
CONF_NAME=create_index.conf
level_num=`grep 'level_num' ${CONF_PATH}${CONF_NAME} | awk -F ":" '{print $2}'`
level_num=`echo $level_num`
level_no=`grep 'level_no' ${CONF_PATH}${CONF_NAME} | awk -F ":" '{print $2}'`
level_no=`echo $level_no`

DESTDATAPATH=/home/video/video_index/data/raw/
DESTDATAFILE=/home/video/video_index/data/raw/raw
DESTDATAFILE_BAK=/home/video/video_index/data/raw_bak/
RESULT_FILE=index_db.txt
MYSQL_PATH=/home/video/database/mysql/
MYSQL_CMD_FILE=../temp/select_indexinfo_indexdb.sql
TEMP_FILE=../temp/indexinfo.txt
SITE_FILE=../conf/vm_site.txt

LINKCLEARMARK_BIN="/home/video/indexdb/bin/linkclearmark"
LINKCLEARMARK_REG="/home/video/indexdb/conf/clearlink.reg"

uniq_no_sort()
{
sort -s -k1,1 -u -T ./ $1 > $TEMP_FILE
sort -t '	' -nrk15,15 -T ./ $TEMP_FILE > $1
}

mv ${DESTDATAPATH}* ${DESTDATAFILE_BAK}

title_count=0

#读取page_table中的内容

#对每一个title_metadata表执行循环
j=0
for((i=0;i<$page_table_num;i++))
do
        page_no=`expr $i + 1`
        if ((`expr $page_no % $level_num` != $level_no))
        then
                continue;
        fi

	TABLE_INDEX=`expr $i + 1`

	rm -rf ${MYSQL_PATH}var/video/$RESULT_FILE	
	rm -rf ${MYSQL_PATH}var/video/${RESULT_FILE}.given	
	
	MYSQL_CMD="select link,(select site from spider_site where spider_url"${TABLE_INDEX}".site_id=spider_site.site_id),'',page_title,player_title,anchor,page_comment,tag,image_sign1,image_sign2,duration,2,0,hot_flag,crt_time,0 into outfile '"$RESULT_FILE"' from spider_url"${TABLE_INDEX}" where flag_dead=0;"

	echo $MYSQL_CMD >$MYSQL_CMD_FILE

	${MYSQL_PATH}bin/mysql -u video -pvideo video<$MYSQL_CMD_FILE

	if [ $? -ne 0 ]
	then
		echo "select indexinfo for index failed!" | mail -s "[select for indexdb error!][VIDEO][${host}][${today}]" ${MAILLIST}
		mv ${DESTDATAFILE_BAK}* ${DESTDATAPATH}
		exit 1
	fi

	line=`wc -l ${MYSQL_PATH}var/video/$RESULT_FILE | awk '{print $1}'`

	if [ $line -eq 0 ]
	then

		echo "indexinfo result file is null!" | mail -s "[select for indexdb error!][VIDEO][${host}][${today}]" ${MAILLIST}
		mv ${DESTDATAFILE_BAK}* ${DESTDATAPATH}
		exit 1
	fi
	
	MYSQL_CMD="select link,(select site from videomap_site where videomap_url"${TABLE_INDEX}".site_id=videomap_site.site_id),'',page_title,player_title,anchor,page_comment,tag,image_sign1,image_sign2,duration,2,0,hot_flag,dist_date,1 into outfile '"${RESULT_FILE}.given"' from videomap_url"${TABLE_INDEX}" where flag_dead=0;"

	echo $MYSQL_CMD >$MYSQL_CMD_FILE

	${MYSQL_PATH}bin/mysql -u video -pvideo video<$MYSQL_CMD_FILE

	if [ $? -ne 0 ]
	then
		echo "select given_page for index failed!" | mail -s "[select for indexdb error!][VIDEO][${host}][${today}]" ${MAILLIST}
		mv ${DESTDATAFILE_BAK}* ${DESTDATAPATH}
		exit 1
	fi
	
	line=`wc -l ${MYSQL_PATH}var/video/${RESULT_FILE}.given | awk '{print $1}'`

	if [ $line -eq 0 ]
	then
		echo "indexinfo result file is null!" | mail -s "[select for indexdb error!][VIDEO][${host}][${today}]" ${MAILLIST}
		mv ${DESTDATAFILE_BAK}* ${DESTDATAPATH}
		exit 1
	fi

	if [ -s $SITE_FILE ]
	then
		awk -v sitetmp="`cat $SITE_FILE`" -F "\t" 'BEGIN{split(sitetmp, site, " ")}{for(i in site){if(site[i]==$2)print $0}}' ${MYSQL_PATH}var/video/${RESULT_FILE}.given > $DESTDATAFILE.${j}
		cat ${MYSQL_PATH}var/video/$RESULT_FILE  >> $DESTDATAFILE.${j}
	else
		mv ${MYSQL_PATH}var/video/$RESULT_FILE $DESTDATAFILE.${j}
	fi
	cat ${MYSQL_PATH}var/video/${RESULT_FILE}.given >> $DESTDATAFILE.${j}

#	下载normal数据的raw文件
	wget ${NORMAL_RAW_SERVER}raw.$i -O $DESTDATAFILE.${j}.normal
	if [ $? -ne 0 ]
	then
		echo "download normal raw file error! path=${NORMAL_RAW_SERVER}raw.$i" | mail -s "[select for indexdb error!][VIDEO][${host}][${today}]" ${MAILLIST}
#		mv ${DESTDATAFILE_BAK}* ${DESTDATAPATH}
		mv ${DESTDATAFILE_BAK}$DESTDATAFILE.${j}.normal ${DESTDATAPATH}
#		exit 1
	fi
	cat $DESTDATAFILE.${j}.normal >>$DESTDATAFILE.${j}

#	uniq_no_sort $DESTDATAFILE.${j}
	mv $DESTDATAFILE.${j} $DESTDATAFILE.${j}.nomerge
	awk -F "\t" 'NF==16{printf "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n",$1,NR,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16}' $DESTDATAFILE.${j}.nomerge| sort -k1,1 -k2,2n -T "./"| ./merge_raw.awk -F "\t"| sed s/'<'/'\&lt;'/g | awk '{printf "%s\t1\n", $0}'|"${LINKCLEARMARK_BIN}" "${LINKCLEARMARK_REG}" 1 17  > $DESTDATAFILE.${j}

	line=`wc -l $DESTDATAFILE.${j} | awk '{print $1}'`
	title_count=`expr $title_count + $line`
	j=`expr $j + 1`
done

rm -rf ${MYSQL_PATH}var/video/$RESULT_FILE	
rm -rf ${MYSQL_PATH}var/video/${RESULT_FILE}.given	

echo "total select indexinfo num for index is :"$title_count | mail -s "[统计][VIDEO][${host}][${today}][全库导出索引数量统计]" ${MAILLIST}

rm $MYSQL_CMD_FILE
exit 0
