#!/bin/bash
set -x
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


