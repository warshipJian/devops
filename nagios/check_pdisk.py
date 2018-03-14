#!/usr/bin/env python
#_*_coding:utf-8_*_

"""
检查dell服务器的硬盘状态，阵列卡状态
"""

#$Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.1 $'

import os
import sys
import subprocess

def usage():
    """显示脚本信息"""
    print """ 
    系统需安装 dell omsa 管理软件
    硬盘的状态值通过 omreport storage pdisk controller = 0 命令获取
    """
    sys.exit(3)

def check_status(val):
    """获取返回给nagios的状态值"""
    if 2 in val :
        status = 2
    elif 1 in val:
        status = 1
    else:
        status = 0
    return status


def split_line(data):
    """把数据拆分为行，并把行按照':'拆分"""
    arg = dict()
    for line in data.split('\n'):
        if ':' not in line:
            continue
        key,val = line.split(':',1)
        arg[key.strip()] = val.strip()
    return arg

def check_pdisk(cid):
    """检查物理磁盘的信息，并进行判断"""
    infos = []
    state = []
    data = os.popen('omreport storage pdisk controller=%s'%cid).read().split('\n\n')
    for val in data:
        if ':' not in val:
            continue
        arg = split_line(val)
        disk_id = arg['ID']
        disk_statu = arg['Status']
        disk_state = arg['State']
        disk_space = arg['Capacity']
        disk_space = disk_space.split()[0] + disk_space.split()[1]       
        disk_pro = arg['Part Number']

        if disk_state == 'Online' and disk_statu == 'Ok':
            status = 0
        else:
            status = 2

        info = 'Disk %s,Status:%s,State:%s,Space:%s,ID:%s'\
        % (disk_id,disk_statu,disk_state,disk_space,disk_pro)

        state.append(status)
        infos.append(info)

    infos = sorted(infos,key=lambda val:val.split(',')[1])
    return state,infos

def get_control_id():
    """获取阵列卡ID,检查阵列卡状态
    阵列卡固件驱动版本低于可更新版本时,显示为降级状态
    该驱动可以不升级,故选择屏蔽该错误"""
    command = subprocess.Popen('omreport', shell=True, stdout=subprocess.PIPE,\
    stderr=subprocess.STDOUT).wait()
    if command != 0:
        usage()

    data = os.popen('omreport storage controller').read()
    arg = split_line(data)

    cid = arg['ID']
    statu = arg['Status']
    state = arg['State']
    mode = arg['Name']
    current_version = arg['Firmware Version']

    try:
        update_version = arg['Latest Available Firmware Version']
    except KeyError:
        update_version = arg['Minimum Required Firmware Version']

    desc = ['OK', 'WARN', 'CRITICAL']

    if statu == 'Ok' and state =='Ready':
        status = 0
    elif current_version != update_version \
    and statu == 'Non-Critical' and state == 'Degraded':
        status = 0
    elif statu == 'Ok' or state =='Ready':
        status = 1
    else:
        status = 2

    return cid,status,"dell controll:%s,Status:%s,State:%s,Mode:%s" % (desc[status],statu,state,mode)

if __name__ == '__main__':
    ID,STAT,INFO = get_control_id()
    STATU,INFOS = check_pdisk(ID)
    STATU.append(STAT)
    STATUS = check_status(STATU)
    INFOS.append(INFO)
    print '\n'.join(INFOS)
    sys.exit(STATUS)
