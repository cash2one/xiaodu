#!/bin/bash
set -x
for((i=0;i<32;i++))
do
str=$str$i","
done
echo $str
