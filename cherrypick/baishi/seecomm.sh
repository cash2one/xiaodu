#!/bin/bash

#awk '{if(FILENAME==ARGV[1]){A[$0]=1;next;} if(FILENAME==ARGV[2]){if(A[$0]==1){print $0;next;}} }' $1 $2 > $3
awk '{if(FILENAME==ARGV[1]){A[$1]=1;next;} if(FILENAME==ARGV[2]){if(A[$1]!=1){print $0;next;}} }' $1 $2 > $3
wc -l $3
