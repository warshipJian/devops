#!/usr/bin/env python
#_*_coding:utf-8_*_


""" 
用于检查服务器负载状态
"""

#$Id$#
__author__ = 'xiaoguo <1165205343@qq.com>'
__version__ = '$Revision: 0.1 $'

import os
import sys

def usage():
    '''脚本用途'''
    print """Usage: check_load \
    show contorller status
    """

def check_load():
    '''获取当前负载状态，获取当前CPU线程数,并进行判断'''
    data = os.popen('cat /proc/loadavg').read().split()
    load1 = float(data[0])
    load5 = float(data[1])
    load15 = float(data[2])

    processer = os.popen("grep 'processor' /proc/cpuinfo | sort -u | wc -l").read().strip('\n')
    proc = float(processer)
    
   
    desc = ['OK', 'WARNING', 'CRITICAL']

    if load15  >= proc + 2  or load1  >= proc + 2:
        status = 2
    elif proc < load15  < proc + 2 :
        status = 1
    else:
        status = 0

    return status,"%s-load average:%.3f,%.3f,%.3f |\
load1=%.3f;%.3f;%.3f;0; load5=%.3f;%.3f;%.3f;0; load15=%.3f;%.3f;%.3f;0;" \
    % (desc[status],load1,load5,load15,load1,proc,proc*2,load5,proc,\
    proc*2,load15,proc,proc*2)

if __name__ == '__main__':

    STATUS,INFO = check_load()

    print INFO

    sys.exit(STATUS)
