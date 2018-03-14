#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
check interface traffic
"""

# $Id$#
__author__ = 'warshipJian'
__version__ = '$Revision: 0.1 $'

import sys
import math
import time
import fcntl
import struct
import socket


def convertbytes(data):
    return int(data) / math.pow(1024, 1)

def ifconfig_bytes():
    traffic_in = dict()
    traffic_out = dict()
    with open('/proc/net/dev') as f:
        for val in f:
            if 'lo' in val:
                continue
            if ':' not in val:
                continue

            _val = val.split(':')

            try:
                ifname = _val[0].strip(':').strip()
                netdata = _val[1].strip(':').strip().split()
                if(len(netdata)) < 8:
                    continue
                if_in = netdata[0]
                if_out = netdata[8]
            except ValueError:
                continue

            traffic_in[ifname] = int(if_in)
            traffic_out[ifname] = int(if_out)

    return traffic_in, traffic_out

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])
    except IOError:
        return None

def ip_type(ip):
    f = struct.unpack('!I', socket.inet_pton(socket.AF_INET, ip))[0]
    private = (
        [2130706432, 4278190080],  # 127.0.0.0,   255.0.0.0   http://tools.ietf.org/html/rfc3330
        [3232235520, 4294901760],  # 192.168.0.0, 255.255.0.0 http://tools.ietf.org/html/rfc1918
        [2886729728, 4293918720],  # 172.16.0.0,  255.240.0.0 http://tools.ietf.org/html/rfc1918
        [167772160, 4278190080],  # 10.0.0.0,    255.0.0.0   http://tools.ietf.org/html/rfc1918
    )
    for net in private:
        if (f & net[1]) == net[0]:
            return True
    return False

def main():
    info = list()
    label = list()
    status = 0

    if_in, if_out = ifconfig_bytes()

    time.sleep(1)

    _if_in, _if_out = ifconfig_bytes()


    for val in if_in:
        ip = get_ip_address(val)
        if ip == None:
            continue
        receive = convertbytes(_if_in[val] - if_in[val])
        transmit = convertbytes(_if_out[val] - if_out[val])
        ptf = '%s receive:%.2fkB/s,transmit:%.2fkB/s' % (val, receive, transmit)
        labe = '%s_receive=%.2f;0;100 %s_transmit=%.2f;0;100' % (val, receive, val, transmit)
        info.append(ptf)
        label.append(labe)
        if(ip_type(ip)):
            if receive >= 50000 or transmit >= 50000:
                status = 2
            elif receive >= 30000 or transmit >= 30000:
                status = 1
        else:
            if receive >= 5000 or transmit >= 5000:
                status = 2
            elif receive >= 3000 or transmit >= 3000:
                status = 1

    print ' '.join(info) + '|' + ' '.join(label)
    sys.exit(status)

if __name__ == '__main__':
    main()
