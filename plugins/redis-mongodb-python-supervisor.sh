#!/bin/bash
#
# 橙石软件部署
#
#
# redis mongodb tmux
#

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
mkdir ~/software

#redis
cd ~/software
if [ ! -f 'redis-3.2.3.tar.gz' ];then
wget http://download.redis.io/releases/redis-3.2.3.tar.gz
fi
tar -xzvf redis-3.2.3.tar.gz
mv redis-3.2.3 /opt/redis
cd /opt/redis
make
make install
mkdir -p /opt/redis/etc/redis
cp redis.conf /opt/redis/etc/redis
sed -i 's/daemonize no/daemonize yes/g'  /opt/redis/etc/redis/redis.conf
sed -i 's/port 6379/port 6389/g'  /opt/redis/etc/redis/redis.conf
nohup /usr/local/bin/redis-server /etc/redis/redis.conf &
if [ "`cat /etc/rc.local | grep redis`" = "" ]; then
    echo "/usr/local/bin/redis-server /opt/redis/etc/redis/redis.conf &" >> /etc/rc.local
fi

#mogodb
cd ~/software
if [ ! -f 'mongodb-linux-x86_64-v3.0-latest.tgz' ];then
wget http://downloads.mongodb.org/linux/mongodb-linux-x86_64-v3.0-latest.tgz?_ga=1.182696294.1753335289.1473401584 -O mongodb-linux-x86_64-v3.0-latest.tgz
fi
tar zxvf mongodb-linux-x86_64-v3.0-latest.tgz
MONGO=`ls | grep mongodb | grep -v "latest.tgz"`
mv "$MONGO" /opt/mongodb
mkdir /opt/mongodb/data
mkdir /opt/mongodb/etc
cat >> /opt/mongodb/etc/mongo.conf <<EOF
dbpath = /opt/mongodb/data
logpath = /opt/mongodb/mongodb.log
pidfilepath = /opt/mongodb/mongodb.pid
directoryperdb = true
port = 27017
EOF
/opt/mongodb/bin/mongod -f /opt/mongodb/etc/mongo.conf --fork &
if [ "`cat /etc/rc.local | grep mongodb`" = "" ]; then
    echo "/opt/mongodb/bin/mongod -f /opt/mongodb/etc/mongo.conf --fork &" >> /etc/rc.local
fi

#python 
cd ~/software
if [ ! -f 'Python-2.7.2.tgz' ];then
wget https://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz
fi
tar zxvf Python-2.7.2.tgz
cd Python-2.7.2
./configure --prefix=/opt/python27  --enable-shared
make
make install
mv /usr/bin/python /usr/bin/python2.6.6
ln -s /opt/python27/bin/python2.7 /usr/bin/python
sed -i 's$#!/usr/bin/python$#!/usr/bin/python2.6$g' /usr/bin/yum
echo "/opt/python27/lib/" >> /etc/ld.so.conf
ldconfig

#pip setuptools
cd ~/software
#/opt/python27/bin/python ez_setup.py 
unzip setuptools-28.0.0.zip
cd setuptools-28.0.0
/opt/python27/bin/python setup.py install

cd ~/software
tar zxvf pip-9.0.1.tar.gz
cd pip-9.0.1
/opt/python27/bin/python setup.py install

#supervisor
cd ~/software
tar zxvf supervisor-3.2.3.tar.gz 
cd supervisor-3.2.3
/opt/python27/bin/python setup.py install
ln -s /opt/python27/bin/supervisor* /usr/bin/
