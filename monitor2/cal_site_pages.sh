#!/bin/bash
set -x
raw_file="/home/video/video_index/data/raw/"
awk -F "/" '{A[$3]++}END{for(x in A)print x"\t"A[x]}' $raw_file/raw.{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31} > site_pages_from_index01.txt
