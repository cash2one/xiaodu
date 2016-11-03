#!/bin/bash
set -x
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/video/php/lib/php/extensions/no-debug-non-zts-20060613
phpbin=~/php/bin/php

if [ $# -ne 2 ];then
	echo "ERROR:usage: ./$0 sitename fileapi"
	exit 1
fi
sitename=$1
fileapi=$2
echo "now start shoulv $sitename urlfileapi[$fileapi] at[`date +%Y%m%d-%H:%M`]"

rm -f ./data/urls_today_$sitename
wget -O ./data/urls_today_$sitename "$fileapi"
if [ $? -ne 0 ];then
	echo "ERROR: wget urlfile failed! site[$sitename] urlfileapi[$fileapi]"
	exit 1
fi
cp ./data/urls_today_$sitename ./data/backup/urls_today_${sitename}_`date +%Y%m%d%H`
echo "wget urlsfile SUC. info[`wc -l ./data/urls_today_${sitename}`]"

#split urls by status
#delete status-1 and status-3 whichi means deleted or droped by site
cat ./data/urls_today_$sitename | awk -F'\t' '{if($1==1 || $1 == 3){print $1"\t"$2} }' > ./data/urls_deadlink
cp ./data/urls_deadlink ./data/backup/urls_deadlink_${sitename}_`date +%Y%m%d%H`
echo "urls need to delete:[`wc -l ./data/urls_deadlink`]"
~/php/bin/php tools_updatedeadlink_dead.php ./data/urls_deadlink "$sitename" > log/updatedeadlink_${sitename}_`date +%Y%m%d%H`
if [ $? -ne 0 ];then
	echo "ERROR: failed to update deadlink into db!"
	exit 1
fi
echo "update deadlink into db SUC!"

#shoulv url into DB parts by parts. each part's url num is low than 1000 and give time 1800 seconds
rm -f ./data/urls_today_${sitename}_*
cat ./data/urls_today_$sitename | awk -F'\t' '{if($1==0){print $2}}' | awk -v site=$sitename 'BEGIN{cnt=0;group=1;} {if(cnt%1000 == 0){group += 1;} cnt+=1; print $0>"./data/urls_today_"site"_"group;}'
echo "cat ./data/urls_today_$sitename | awk -F'\t' '{if($1==0){print $2}}' | awk -v site=$sitename 'BEGIN{cnt=0;group=1;} {if(cnt%1000 == 0){group += 1;} cnt+=1; print $0>"./data/urls_today_"site"_"group;}'"
echo "split urls into parts info[`wc -l ./data/urls_today_${sitename}_*`]"

files=`ls ./data/urls_today_${sitename}_*`
for file in $files
do
	echo "now process [$file] at [`date +%Y%m%d-%H:%M`]"
	#clean last process if it has not Done
	echo "befor clean, ps info:"
	ps -ef | grep "shoulv_start.php" | grep "$sitename"
	pids=`ps -ef | grep "shoulv_start.php" | grep "$sitename" | awk '{print $2}' `
	echo "pids:[$pids]"
	if [ "$pids" != "" ];then
		kill -9 $pids
	fi

	echo "after clean: ps info:"
	ps -ef | grep "shoulv_start.php" | grep "$sitename"
	#start process
	mv $file ./data/urls_$sitename
	$phpbin shoulv_start.php $sitename >> log/shoulv_${sitename}_`date +%Y%m%d%H%M` &

	sleep 3
	#max interval is 1800 seconds
	maxsec=1600
	while [ $maxsec -gt 11 ]
	do
		maxsec=`expr $maxsec - 10`
		#process Done
		pids=`ps -ef | grep "shoulv_start.php" | grep "$sitename" | awk '{print $2}' `
		if [ "$pids" == "" ];then
			echo "last process has been done"
			break;
		fi
		sleep 10
	done
done
