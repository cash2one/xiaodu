#!/bin/bash

while [ 2 -gt 1 ]
do
	sh baipinghui_convert_ctl.sh >> log/baipinghui_convert.log
	sleep 300
done
