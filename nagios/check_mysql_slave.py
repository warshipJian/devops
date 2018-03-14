#!/usr/bin/env python
#_*_coding:utf-8_*_

""" 
用于检查数据库主从同步状态
"""

#$Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.1 $'

import os
import sys
import time
import getopt

def usage():
    """脚本使用方法"""
    print """Usage: check_mysql_slave [-h|--help] 
	[-r | --room  ] [-i | --ip ] [-p | --port ] 
	example: %s -r gz -p 33605 -i 192.168.1.115 """ % sys.argv[0]
    sys.exit(3)

def check_status(state):
    """对状态进行检查"""
    if 2 in state:
        status = 2
    elif 1 in state:
        status = 1
    else:
        status = 0
    return status

def status_report(room,ip,port):
    """判断主从同步状态，延迟大于600为严重状态"""	
    arg = dict()

    #if os.path.exists('/opt/monitor/mysql/%smysql_slave_%s_%s.status' % (room,ip,port)):
    #    fp = '/opt/monitor/mysql/%smysql_slave_%s_%s.status' % (room,ip,port)
    #    _fp = file(fp)
    #elif os.path.exists('/opt/monitor/mysql/%smysql_master_%s_%s.status' % (room,ip,port)):
    #    fp = '/opt/monitor/mysql/%smysql_master_%s_%s.status' % (room,ip,port)
    #    _fp = file(fp)
    #else:
    #    fp = '%s_mysql_(master/slave)_%s_%s.status' % (room,ip,port)
    #    print 'file %s not exist'% fp
    #    sys.exit(2)
    passwd = '123Dianjia$%^' 
    command = "mysql -uroot -p%s -h%s -e 'show slave status\G'" %(passwd,ip)
    _fp = os.popen(command).readlines()

    for line in _fp:
        try:
            key,val = line.strip().split(':',1)
        except ValueError:
            continue

        arg[key] = val

    if arg == {}:
        status = 2
        return status,"%s ip:%s port:%s no monitor data!" % (room,ip,port)

    try:
        io_running = arg['Slave_IO_Running'].strip()
        sql_running = arg['Slave_SQL_Running'].strip()
        seconds_behind_master = int(arg['Seconds_Behind_Master'].strip())	
    except KeyError:
        try:
            seconds_behind_master = arg['Seconds_Behind_Master'].strip()
            status = 2
            return status,"%s ip:%s port:%s Seconds_Behind_Master:%s" % \
            (room,ip,port,seconds_behind_master)
        except KeyError:
            status = 2
            return status,"%s ip:%s port:%s no Seconds_Behind_Master!" % (room,ip,port)
    if io_running == 'Yes' and sql_running == 'Yes' and seconds_behind_master <=30:
        status = 0
        return status, "%s ip:%s port:%s Seconds_Behind_Master:%s" % \
        (room,ip,port,seconds_behind_master)	
    elif io_running == 'Yes' and sql_running == 'Yes' and seconds_behind_master <=1200:
        status = 1
        return status, "%s ip:%s port:%s Seconds_Behind_Master:%s" % \
        (room,ip,port,seconds_behind_master)        
    else:
        status = 2
        return status, "%s ip:%s port:%s Seconds_Behind_Master:%s io_running:%s sql_running:%s" % \
        (room,ip,port,seconds_behind_master,io_running,sql_running)

def check_slave(room,ip,port):
    """检查mysql 同步状态"""
    try:
        status,desc = status_report(room,ip,port)
    except ValueError:
        status = 2
        desc = '%s ip:%s port:%s please check %s_mysql_master/slave_%s_%s_status'\
                % (room,ip,port,room,ip,port)
    return desc,status

def get_room_ip_port():
    """获取机房，服务器ip，mysql端口"""
    try:
        opts,_ = getopt.getopt(sys.argv[1:], "hr:i:p:", ["help","room","ip", "port"])
	room = ''
        if opts == []:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exiti(2)
            elif opt in ("-r", "--room"):
                if arg == 'lan' or arg =='aws':
                    room = arg
            elif opt in ("-i","ip"):
                ip = arg
            elif opt in ("-p", "port"):
                try:    
                    port = int(arg)
                except ValueError:      
                    print 'please input mysql port, more information: --help'
                    sys.exit(2)
            else:
                usage()       
                sys.exit(2)
        return room,ip,port
    except getopt.GetoptError:
        usage()        
        sys.exit(2)

if __name__ == '__main__':
    ROOM,IP,PORT = get_room_ip_port()
    ERROR,STATUS = check_slave(ROOM,IP,PORT)    
    print ERROR
    sys.exit(STATUS)
