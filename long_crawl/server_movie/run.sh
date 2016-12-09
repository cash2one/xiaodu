#!/bin/bash

export LD_LIBRARY_PATH=/home/video/database/mysql/lib/mysql:$LD_LIBRARY_PATH
py_bin="/home/video/install/python27/bin/python"
nohup $py_bin ./bll/MOVIE_DBControl.py >/dev/null &

exit 0

