# monitor
## deploy
0 9 * * * cd /home/video/shangshuaipeng/pgc_ec/monitor && ~/.jumbo/bin/python toutiao_daily_mail.py &>toutiao_mail.ct.log
## 报表mail
```
PGC抓取情况 year-month-day
昨日新增用户
昨日新增obj
已抓用户总量
已抓obj总量

db: ec_task
select count(*) from user_result where site_id=8
select count(*) from obj_result where site_id=8
select count(*) from user_result where site_id=8 and create_time >= "2016-07-05" and create_time < "2016-07-06"
select count(*) from obj_result where site_id=8 and create_time >= "2016-07-05" and create_time < "2016-07-06"

```
