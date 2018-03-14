#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
check centos 6 iptables status
"""

# $Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.1 $'

import os
import sys

def main():
    hostType = 1
    status = 2
    state = 2
    if os.path.exists('/var/lock/subsys/iptables'):
        status = 0
        state = 0
    if os.path.exists('/var/lock/subsys/libvirtd'):
        hostType = 0
        state = 0
    iptablesDesc = ['running','','not running']
    hostDesc = ['physics','kvm']
    print ('iptables is %s , host type is %s' % (iptablesDesc[status],hostDesc[hostType]))
    sys.exit(state)

if __name__ == '__main__':
    main()