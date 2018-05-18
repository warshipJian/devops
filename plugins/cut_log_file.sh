#!/bin/bash
LogFile="/apps/$1/nohup.out"
HostName=$(hostname)

# 计算日期,保留3天之内的
Day=`date -d'-3 day'  "+%Y-%m-%d"`
Line=`grep -n "^\[$Day" $LogFile | head -n 1  | cut  -d  ":"  -f  1`

# 删除之前的
if [ ! -n "$Line" ]; then
        echo > $LogFile
else
        sed -i "1,${Line}d" $LogFile
fi
