#!/bin/bash

export LD_LIBRARY_PATH=/home/video/database/mysql/lib/mysql:$LD_LIBRARY_PATH
py_bin="/home/video/install/python27/bin/python"
nohup $py_bin ./bll/DBControl.py >>exe.log &

exit 0

