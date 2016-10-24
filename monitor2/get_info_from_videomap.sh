#!/bin/bash
set -x
>$2
while read line
do
sign1=`echo $line | awk '{print $2}'`
sign2=`echo $line | awk '{print $3}'`
sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`

result=`/home/video/database/mysql/bin/mysql -u root video -e "select link,duration from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2"`
echo "$result">>$2
done <$1
