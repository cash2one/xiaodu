#!/bin/bash


set -x

if [ $# -ne 1 ]
then
	echo "./cover_test.sh input_file"
	exit 1

fi

> result.txt
while read i
do
	./url_page_index.sh "${i}" > tmp.txt
	awk '$>>"result.txt"}' tmp.txt





done < $1
