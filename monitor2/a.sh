#!/bin/bash
set -x
> valid_our_site_num.txt
while read i
do
	awk  '$1=="'$i'"{print $0}' site_add.txt >> valid_our_site_num.txt
done < main_valid_site.txt

sort -k2,2 -nr valid_our_site_num.txt > tmp

mv tmp  valid_our_site_num.txt
