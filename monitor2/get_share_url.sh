#!/bin/bash

set -x
#cd ~/../video/video_hindex/data/raw


#awk -F "\t" 'NR==FNR{site[$0]=1;next}site[$2]!=1&&a[$2]<100{a[$2]++;print $1"\t"$2}' ../../conf/filtsite.txt raw.[0-9] raw.[0-9][0-9] > ~/share_video.txt
./mysql -u root video -e "select site from spider_site where page_num > 100" | awk 'NR>1{print}' > fs_site.txt

./mysql -u root video -e "select site from videomap_site where page_num" | awk 'NR>1{print}' >> fs_site.txt

sort -u fs_site.txt > tmp.txt

mv tmp.txt fs_site.txt



time_line=`date -d '3 week ago' +%s`
./mysql -u root video -e "select link,(select site from spider_site where spider_url1.site_id=spider_site.site_id) from spider_url1 where crt_time > $time_line and flag_dead=0" | awk 'NR>1{print}' > link.txt

./mysql -u root video -e "select link,(select site from videomap_site where videomap_url1.site_id=videomap_site.site_id) from videomap_url1 where crt_time > $time_line and flag_dead=0" | awk 'NR>1{print}' >> link.txt

sort -u -T ./ link.txt > tmp.txt

mv tmp.txt link.txt

awk -F "\t" 'NR==FNR{a[$0]=1;next}a[$2]==1{print}' fs_site.txt link.txt > 1.txt

awk -F "\t" 'NR==FNR{a[$0]=1;next}a[$2]!=1{print}' ../video/video_index/conf/filtsite.txt 1.txt > 2.txt

awk -F "\t" 'a[$2]<100{a[$2]++;print}' 2.txt > share_video.txt

sort -t '	' -k2,2 -u ~/share_video.txt | wc -l
