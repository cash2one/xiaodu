source ~/.bashrc
DT=`date +'%Y%m%d'`
#all_info.log大小读取
while [ 1 ]
do
rm /home/video/vor_realtime/uniq_simid/data_compute.log*
if [ $? -ne 0 ]
then
        echo ${DT} 'data_compute.log* clean fail.'
        exit 2
fi
NOHUP_SIZE=`du -m /home/video/vor_realtime/uniq_simid/nohup.out | awk '{print $1}'`
if [ $? -ne 0 ]
then
        echo ${DT} 'nohup.out size read fail.'
        exit 2
fi
#超过200M清空
if [ ${NOHUP_SIZE} -gt 200 ]
        then
                echo > /home/video/vor_realtime/uniq_simid/nohup.out
                if [ $? -ne 0 ]; then
                        echo ${DT} 'nohup.out clean fail.'
                        exit 2
                fi
                echo `date +%Y/%m/%d-%H:%M` "nohup.out clean success."
fi
sleep 3600
done
