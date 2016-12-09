site=(ku6.com pptv.com baomihua.com v1.cn aipai.com boosj.com 56.com tangdou.com yinyuetai.com wasu.cn le.com fun.tv)

for sitename in ${site[@]}  #等价于  for i in ${city[*]}
do
        python http_code.py $sitename
        sleep 1
done
