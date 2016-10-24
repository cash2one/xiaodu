#!/bin/bash
set -x
while read line
do
sign1=`./print_sign "$line" | awk '{print $1}'`
sign1=`echo $sign1`
sign2=`./print_sign "$line" | awk '{print $2}'`
sign2=`echo $sign2`
sum=`expr $sign1 + $sign2`
index=`expr $sum % 64`
index=`expr $index + 1`
result=`~/mysql -u root video -e "select count(*) from spider_url${index} where link_sign1=$sign1 and link_sign2=$sign2\G" | awk '{if(NR>1)print $0}' | awk '{print $2}'`
result=`echo $result`
if((result==1))
then
echo -e "$line" >> $2
fi
done<$1
