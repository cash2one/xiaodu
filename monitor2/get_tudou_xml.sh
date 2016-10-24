#!/bin/bash
set -x
i=1
while(($i==1))
do
	j=0
	while [ $j -lt 3 ]	
	do
		wget "http://tdsearch:2012search01061329@export.tudou.com:80/pri/public/itemlastest.xml" -O /home/rd/apache/htdocs/tudou_videomap/itemlastest.xml
		if [ $? -eq 0 ] ;then
			break;
		fi
		$j=`expr $j + 1`
	done
	sleep 270
done
