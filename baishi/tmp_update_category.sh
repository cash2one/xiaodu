#!/bin/bash

file_cid_ctid=$1
file_ctid_ctname=$2
file_cid_url=$3

awk -F'\t' '{
	if(FILENAME==ARGV[1]){ cc[$1]=$2;next; } 
	if(FILENAME==ARGV[2]){ if($5 == 1){c1n[$1]=$2;next;} if($5 == 2){c2n[$1]=$2;next;} if($5>=3){c3n[$1]=$2;next} print "bad line"$0 ;next;} 
	if(FILENAME==ARGV[3]){ if($1 in cc){ccid=cc[$1]; print $2"\t"c1n[ccid]"\t"c2n[ccid]"\t"c3n[ccid];} else{print "no info:"$0;} } 
	}' $file_cid_ctid $file_ctid_ctname $file_cid_url
	
#if(FILENAME==ARGV[3]){ print $0;if($1 in cc){ccid=cc[$1]; print $2"\t"c1[ccid]"\t"c2n[ccid]"\t"c3n[ccid];} else{print "no info:"$0;} } 
