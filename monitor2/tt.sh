#!/bin/bash
set -x
> have.txt
> no.txt
while read i
do
	ccl=`./url_page_index.sh "$i" | grep "link:" | wc -l`
	if [ $ccl -gt 0 ]
	then
		echo $i >>have.txt
	else
		echo $i >> no.txt
	fi

done < z.txt 
