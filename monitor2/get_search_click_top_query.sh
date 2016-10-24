cd /home/video/q_url

set -x

day=`date -d'1 days ago' +%Y%m%d`
if [ $1 ]
then
    day="$1"
fi

echo -e "fid\tqurey\tquery_num\tclick_num\tfirstpage_click_num\tfirstpage_query_num" 

wget -nv "http://logdata.baidu.com/?m=Data&a=GetData&token=video_k65jmeo43v7tnfsbu9gzwacxpq&product=video&type=normal&item=video_fid_search_query_and_click_file&date=$day" -O queryclick


awk -F'\t' '{
	q[$2]+=$3;
	c[$2]+=$4;
	fc[$2]+=$5;
	fp[$2]+=$6;
}END{
	for(i in q)
	{
		if(!q[i])
		  q[i]=1;
		if(!c[i])
		  c[i]=1;
		if(!fp[i])
		  fp[i]=1;
		rate=sprintf("%.2f\t%.2f\t%.2f",fc[i]/fp[i],fp[i]/q[i],fc[i]/c[i]);
		print i"\t"q[i]"\t"c[i]"\t"fc[i]"\t"fp[i]"\t"rate;
		#print i"\t"q[i]"\t"c[i]
	}
}' queryclick > queryclick.nofid

sort -t'	' -k3nr queryclick.nofid > queryclick.click
sort -t'	' -k2nr queryclick.nofid > queryclick.query

subject="topµã»÷$day  query pv click firstclick firstpv" 


head -100 queryclick.click  | awk -F'\t' -vsubject="$subject" 'BEGIN{
	print "From:video@tc-video-ld00.tc.baidu.com"
	print "To:video-search-rd@baidu.com video-rec-rd@baidu.com"
	print "Subject:"subject
	print "Mime-Version: 1.0"
	print "Content-Type: text/html; charset=gb2312"
	print "<html>"
	print "<body>"
	print "ftp://tc-video-ld00.tc.baidu.com:/home/video/q_url/queryclick.click"
	print "<table border=1>	"
}{
	print "<tr>"
	for(i=1;i<=NF;++i)
	{
		if($(NF-1) < 0.8 || $NF < 0.8)
			print "<td><red>"$i"</red></td>"
	else
			print "<td>"$i"</td>"
	}
	print "</tr>"
}END{
	print "</table>"
	print "</body>"
	print "</html>"
}'  > queryclick.html 
cat queryclick.html | /usr/sbin/sendmail -t

subject="top¼ìË÷$day  query pv click" 

head -100 queryclick.query  | awk -F'\t' -vsubject="$subject" 'BEGIN{
	print "From:video@tc-video-ld00.tc.baidu.com"
	print "To:video-search-rd@baidu.com video-rec-rd@baidu.com"
	print "Subject:"subject
	print "Mime-Version: 1.0"
	print "Content-Type: text/html; charset=gb2312"
	print "<html>"
	print "<body>"
	print "ftp://tc-video-ld00.tc.baidu.com:/home/video/q_url/queryclick.query"
	print "<table border=1>	"
}{
	print "<tr>"
	for(i=1;i<=NF;++i)
	{
		print "<td>"$i"</td>"
	}
	print "</tr>"
}END{
	print "</table>"
	print "</body>"
	print "</html>"
}'  > queryclick.query.html 
cat queryclick.query.html | /usr/sbin/sendmail -t
