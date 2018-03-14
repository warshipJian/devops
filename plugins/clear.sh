#!/bin/bash
max=60
min=30
for i in `seq 1 $max`
do
    if [ $i -ge 30 ];then
        pricingName=`/usr/bin/find /opt/mysqlbak/pricing/* -mtime +${i} | tail -1`
        if [ "$pricingName" != "" ];then
            mv $pricingName /opt/mysqlbak/old/pricing
        fi
        futuresName=`/usr/bin/find /opt/mysqlbak/futures/* -mtime +${i} | tail -1`
        if [ "$futuresName" != "" ];then
            mv $futuresName /opt/mysqlbak/old/pricing
        fi
    fi
done
/usr/bin/find /opt/mysqlbak/* -mtime +$min  -type f -name *.tar.bz2 | xargs /bin/rm -fr
