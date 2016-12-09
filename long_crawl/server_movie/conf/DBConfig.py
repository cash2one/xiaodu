# -*- encoding:utf8 -*-
class DBConfig(object):
    MYSQL = {
            "host":"10.36.3.207",
            "db_name":"ns_video",
            "uname":"ns_video_w",
            "pwd":"aLPpt59INnr37aKP",
            "encoding":"gbk",
            "port":6043
           }
    REDIS = {
            "linklist_queue":{"host":"10.36.64.60", "port":9379, "db":12},
            "cache_queue":{"host":"10.36.64.60", "port":9379, "db":13},
            "dataobj_queue":{"host":"10.36.64.60", "port":9379, "db":14},
            "monitor_queue":{"host":"10.36.64.60", "port":9379, "db":15}
            }
