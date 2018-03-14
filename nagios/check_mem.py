#!/usr/bin/env python
#_*_coding:utf-8_*_

"""
检查服务器内存使用情况
"""

#$Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.1 $'


import sys
import check_dell 

def usage():
    """通过/proc/meminfo文件获取服务器的内存使用信息"""
    print """Usage: check_mem.py"""
    sys.exit(3)

def get_mem():
    """获取/proc/meminfo/的信息"""
    mem = dict()
    data = file('/proc/meminfo').readlines()
    for val in data:
        key = val.split(':')[0].strip()
        value = int(val.split(':')[1].split()[0])/1024
        mem[key] = value

    return mem

def check_mem():
    """检查内存使用情况,返回剩余的物理内存"""
    mem = get_mem()
    memtotal = mem['MemTotal']
    memfree = mem['MemFree']
    buffers = mem['Buffers']
    cached = mem['Cached']
    memrefree = memfree + buffers + cached
    percent = (float(memrefree)/memtotal)*100
    percent = float('%.2f' % percent)

    return memtotal,memrefree,percent

def main():
    """返回信息到nagios"""
    memtotal,memrefree,percent = check_mem()

    if percent <= 0.02:
        status = 2
    elif percent <= 0.05:
        status = 1
    else:
        status = 0

    try:
        info,state = check_dell.get_mem() 
        if state != 'Ok':
            status = 2
    except KeyError:
            status = status

    desc = ['OK','WARNING','CRITICAL']

    info = "Memstatus:%s,MemFree:%dMB,MemTotal:%dMB free:%s%% |label=%d;%d;%d" % \
    (desc[status],memrefree,memtotal,percent,memrefree,0,memtotal)
    return status,info

if __name__ == "__main__":
    STATUS,INFO = main()
    print INFO
    sys.exit(STATUS)
