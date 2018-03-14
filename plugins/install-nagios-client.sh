#!/bin/bash
useradd nagios
groupadd nagios

tar zxvf nagios-plugins-2.1.1.tar.gz
cd nagios-plugins-2.1.1
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
make install
cd ..

tar zxvf nrpe-2.15.tar.gz
cd nrpe-2.15
./configure --enable-command-args
make all
make install-plugin
make install-daemon
make install-daemon-config
cd ..

cp python-plugins/*.py /usr/local/nagios/libexec/
cp nrpe.cfg /usr/local/nagios/etc/ 
cp nrpe /etc/init.d/
chmod +x /etc/init.d/nrpe
service nrpe start
