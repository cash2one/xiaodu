#!/bin/bash

cd /home/rd/
set -x

if [ $# -ne 1 ]
then
	echo "./cover_test.sh input_file"
	exit 1

fi

#awk '$0~"^http://www.tudou.com/programs/view/"&&$0!`"/$"{print $0"/"}' $1 > tmp.txt

#mv tmp.txt $1

> result.txt
while read i
do
	i=`echo $i`
	if [ "${i}" == "" ]
	then
		continue
	fi
	./url_page_index.sh "${i}" > tmp.txt
	#spider和videomap都有的是3
	awk 'BEGIN{begin_our=0;y=0}$0~"^spider_url"{begin_our=1}begin_our==1&&$0~"page_id"{y=1}$0~"^videomap_url"{begin_our=2}begin_our==2&&$0~"page_id"{if(y==1) y=3;else y=2}END{print "'${i}'""\t"y}' tmp.txt >> result.txt
	#./make_res.py tmp.txt "${i}" 1
done < $1
exit

scp result.txt video@tc-video-ct0.tc:~/cover_cal/

ssh video@tc-video-ct0.tc "cd /home/video/cover_cal;sh +x /home/video/cover_cal/cover_test.sh;"

scp video@tc-video-ct0.tc:~/cover_cal/c.txt .

#awk -F "\t" '$2==0{print $1}' c.txt > not_in_link.txt
awk -F "\t" '$2==0||$2==-100{print $1}' c.txt > not_in_link.txt
#查找网页库是否收录
scp not_in_link.txt vsspider@jx-map-spi01.jx:wcy/bailing_tool/shell

ssh vsspider@jx-map-spi01.jx "cd /home/vsspider/wcy/bailing_tool/shell;mv not_in_link.txt url.txt; ./is_url_in.sh;"

scp vsspider@jx-map-spi01.jx:wcy/bailing_tool/shell/have.txt .

sort -k2,2 have.txt > tmp.txt

mv tmp.txt have.txt
echo "1" >>  have.txt
awk -F "\t" 'NR==FNR{a[$1]=1;next}a[$1]==1{print $1"\t-101";next}{print}' have.txt c.txt > d.txt

cat d.txt
