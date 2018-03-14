#!/usr/bin/env python
# coding:utf8
''' check supervisord status'''

import re
import sys

def check(pidfile):
    ''' daemon'''
    name = pidfile.split('/')[-1].rstrip('.pid')
    ok = 'ok, %s is running' % name
    err = 'critical! %s is not running' % name
    try:
        pid = file(pidfile).read().strip()
    except IOError:
        print err
        return 2
    try:
        stat = file('/proc/%s/stat' % pid).read()
    except IOError:
        print err
        return 2
    if re.search('z|Z',stat.split()[2]):
        print err
        return 2
    else:
        print ok
        return 0

def main():
    status = []
    for val in ['/tmp/supervisord.pid','/var/run/crond.pid']:
    	status.append(check(val))
    if 2 in status:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
