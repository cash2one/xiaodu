#!/bin/bash

wget $1 -O /home/rd/apache/htdocs/temp.xml
/home/rd/apache/cgi-bin/xmltest [0] /home/rd/apache/htdocs/temp.xml
sleep 10
cat /home/rd/apache/cgi-bin/result_news.txt | sed 's/$/\<br\>/g'  > /home/rd/apache/cgi-bin/result.txt 
echo `cat /home/rd/apache/cgi-bin/result.txt`
