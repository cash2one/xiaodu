echo `date +%Y/%m/%d-%H:%M` "get oldmd5 for data start."
oldmd5=`md5 -r ./http_status.sh|awk  -F ' ' '{print $1}'`
echo `date +%Y/%m/%d-%H:%M` ${oldmd5} "get oldmd5 for data end."
while [ 1 ]
do 
	echo `date +%Y/%m/%d-%H:%M` "get newmd5 for data start."
	newmd5=`md5 -r ./http_status.sh|awk  -F ' ' '{print $1}'`
	echo `date +%Y/%m/%d-%H:%M` $newmd5 "get newmd5 for data end."
	echo `date +%Y/%m/%d-%H:%M` "newmd5 vs oldmd5 is same ? start. newmd5: " $newmd5", oldmd5: "$oldmd5
	if [ ${oldmd5}==${newmd5} ]
	then
		echo `date +%Y/%m/%d-%H:%M` "newmd5 vs oldmd5 is same, end. and return now."
		#sleep 300
		#continue
		break
	fi
done
