#source /etc/profile
WORK_DIR=`pwd`
DATA_DIR=${WORK_DIR}/script
SPIDER_DIR=${WORK_DIR}/spider_data
PROJECT_NAME=$1

#1.获取配置文件
#echo ${DATA_DIR}
#2.获取工程数据文件
sh fetch_data.sh ${PROJECT_NAME} ${DATA_DIR}
if [ $? -ne 0 ];then
    echo ${PROJECT_NAME} 'fetch_data fail'
    exit 2
fi

#数据计算+冲图
cat ${SPIDER_DIR}/${PROJECT_NAME}.res | python invokePluginMain.py ${PROJECT_NAME}
if [ $? -ne 0 ];then
   echo ${PROJECT_NAME} 'invokePluginMain fail'
   exit 3
fi
