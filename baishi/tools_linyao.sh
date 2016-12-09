#!/bin/bash

if [ $# -ne 2 ];then
	echo "usage: ./$0 link_or_sign64 flag_linkorsign64"
	exit 1
fi

~/odp/php/bin/php tools_caculate_tblnum_withsign.php "$1" $2

tail -2 ./conf/db.conf*
