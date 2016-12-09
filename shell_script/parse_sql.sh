files=`ls ./sql/*`
for file in ${files}  #等价于  for i in ${city[*]}
do
        filename=${file##*/}
        echo $filename
        cat $file | awk -F "='" '{print $7,$8}' | awk -F "', real_link" '{print $1"\t"$2}' | awk -F "', file_type" '{print $1}' >> ./links/${filename}
        sleep 0.4
done
