#!/bin/bash
#
#

#redis
mkdir ~/software
cd ~/software
if [ ! -f 'phpredis-2.2.7.tar.gz' ];then
    wget https://codeload.github.com/phpredis/phpredis/tar.gz/2.2.7 -O phpredis-2.2.7.tar.gz 
fi
tar zxvf phpredis-2.2.7.tar.gz
cd phpredis-2.2.7
/usr/local/php/bin/phpize 
./configure --with-php-config=/usr/local/php/bin/php-config
make
make install

#mongodb
cd ~/software
if [ ! -f 'mongo-1.6.14.tgz' ];then
    wget https://pecl.php.net/get/mongo-1.6.14.tgz
fi
tar zxvf mongo-1.6.14.tgz 
cd mongo-1.6.14
/usr/local/php/bin/phpize 
./configure --enable-mongo=share --with-php-config=/usr/local/php/bin/php-config
make
make install

#swoole
cd ~/software
if [ ! -f 'swoole-1.8.11.tgz' ];then
    wget https://pecl.php.net/get/swoole-1.8.11.tgz
fi
tar zxvf swoole-1.8.11.tgz
cd swoole-1.8.11
/usr/local/php/bin/phpize 
./configure  --with-php-config=/usr/local/php/bin/php-config
make
make install

#other extend
cd /root/software/lnmp1.3/src
tar zxvf php-5.6.22.tar.gz
PHPEXT="/root/software/lnmp1.3/src/php-5.6.22/ext"
cd $PHPEXT/fileinfo
/usr/local/php/bin/phpize 
./configure --with-php-config=/usr/local/php/bin/php-config
make
make install

#
#cd $PHPEXT/pdo_dblib
#/usr/local/php/bin/phpize 
#./configure --with-php-config=/usr/local/php/bin/php-config
#make
#make install
#

#config php.ini
PHPINI="/usr/local/php/etc/php.ini"
CONFIG="extension=redis.so
extension=mongo.so
extension=fileinfo.so
extension=swoole.so"
if [ "`cat $PHPINI | grep 'extension=mongo.so'`" = "" ]; then
    echo "$CONFIG" >> $PHPINI  
fi

#restart php service
service php-fpm restart

#install composer
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('SHA384', 'composer-setup.php') === 'e115a8dc7871f15d853148a7fbac7da27d6c0030b848d9b3dc09e2a0388afed865e6a3d6b3c0fad45c48e2b5fc1196ae') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"

