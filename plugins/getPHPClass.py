#!/usr/bin/env python
#coding:utf8

import sys

f = open('class.php', 'rt')
data = f.readlines()
f.close()

classData = []
className = None
for v in data:
    v = v.strip('\n')
    if v == '':
        continue
    classData.append(v)
    if len(v) > 5:
        #第一行
        if 'class' == v[0:5]:
            # 获取类名
            k = v.split()
            className = k[1]
    elif '}' == v[0]:
        #类结束
        if className:
            thefile = open('../' +className + '.php', 'w')
            thefile.write("<?php\n")
            thefile.write("namespace WarshipJian\Getui\igetui\\base;\n")
            thefile.write('\n')
            thefile.write('use WarshipJian\Getui\protobuf\PBMessage;\n')
            for item in classData:
                thefile.write("%s\n" % item)
            thefile.close()
            classData = []
            className = None
