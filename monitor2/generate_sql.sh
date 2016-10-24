#!/bin/bash
set -x
while read line
do

url=`echo $line | awk '{print $1}'`
new_url=$url"/"

sign1=`./print_sign "$url" | awk '{print $1}'`
sign1=`echo $sign1`
sign2=`./print_sign "$url" | awk '{print $2}'`
sign2=`echo $sign2`
sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`

new_sign1=`./print_sign "$new_url" | awk '{print $1}'`
new_sign1=`echo $new_sign1`
new_sign2=`./print_sign "$new_url" | awk '{print $2}'`
new_sign2=`echo $new_sign2`
new_sum=`expr $new_sign1 + $new_sign2`
new_index=`expr $new_sum % 64`
new_index=`expr $new_index + 1`

echo "update spider_url"$index" set flag_dead=2,dead_check_time=1251216000,link_status=-1 where link_sign1=$sign1 and link_sign2=$sign2 and link_status=0 and exists (select link_sign1 from spider_url"$new_index" where link_sign1=$new_sign1 and link_sign2=$new_sign2);" >> $2

done<$1
