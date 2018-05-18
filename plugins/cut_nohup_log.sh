#!/bin/bash
LogFile="/apps/$1/nohup.out"
cp $LogFile /apps/$1/logbak
echo '' > $LogFile
cd /apps/$1/logbak
mv nohup.out $(date +%F).nohup.out
find ./ -mtime +3 | xargs -n 1 rm -f
