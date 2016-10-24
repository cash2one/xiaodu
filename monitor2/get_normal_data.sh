#!/bin/bash
set -x

awk -F "\t" '$3!=""&&a[$2]<5{a[$2]++;print $2"\t"$3"\t"$11"\t"$1}END{for(x in a)if(a[x]==5)print x >> "valid_site.txt"}' /home/video/video_index/data/raw/raw.* > need_check_normal.txt.tmp

awk -F "\t" 'FILENAME=="valid_site.txt"{a[$0]=1;next}a[$1]==1{print $0}' valid_site.txt need_check_normal.txt.tmp > need_check_normal.txt 


