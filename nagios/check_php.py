#!/usr/bin/python
#_*_coding:utf-8_*_


""" 
check host SSH port,check host ping status
"""

#$Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.2 $'
  
import os
import sys
import socket


def check_ssh(ip,port):
    """check ssh port status,check ip status"""

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)

    try:
        sk.connect((ip,port))
        status = 0
        con = 0
    except socket.error:
        status = 2
        con = 1         
        #trac = tracert(ip)
    sk.close()

    desc = ['OK','WARNING','CRITIACAL']
   
    return status,"ip:%s port:%s %s" % (ip,port,desc[status])

def main():
    """return infos to nagios"""
    port = 9989
    ips = '127.0.0.1'
    status,inf = check_ssh(ips,int(port))
         
    return inf,status

if __name__ == "__main__":
    INFO,STATE = main()
    print INFO
    sys.exit(STATE)
