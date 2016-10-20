project_name=$1
spider_script_dir=$2
#echo ${spider_script_dir}
cd $spider_script_dir && sh download.sh $project_name
if [ $? -ne 0 ];then
    echo 'download ${project_name} data fail'
    exit 1
fi

