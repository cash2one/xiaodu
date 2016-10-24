def mail(sender,receiver,subject,content):
    mail_body="""From:%s
To:%s
Subject:%s
Mime-Version: 1.0
Content-Type: text/html; charset=gb2312
        %s
        """ % (sender,receiver,subject,content)
                       
    os.system("echo '%s' | /usr/sbin/sendmail -t" % (mail_body))
if __name__ == "__main__" :
    mail("jiangyuqin@baidu.com","jiangyuqin@baidu.com","[VIDEO]建库每日模块运行时间表",html)
