for i in `cat sites.txt`
do
STATUS_CODE=`curl -o /dev/null -s -w %{http_code} $i`
echo  "${i}:\t${STATUS_CODE}"
done
