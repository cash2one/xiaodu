for i in `seq 1 37`
do
    wget -q ftp://tc-video-lcminer0.tc.baidu.com/home/video/letv/data/raw_$i.txt -O le.data
    nohup ~/odp/php/bin/php shoulv_le_tmp.php
done
