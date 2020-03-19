# tools 此项集成了各类脚本工具

## [utility.py](/utility.py)
用python实现的一些常用的工具方法

## [virsh_manage.py](/virsh_manage.py)
利用virsh命令管理虚拟机的接口

## [ocata-all-in-one.sh](/ocata-all-in-one.sh)
kolla-ansible 安装部署openstack ocata版本的命令脚本

## [mon_scripts.sh](mon_scripts.sh)
此脚本用户监控服务负载，保存服务器高负载时的状况快照

## [mysql-opertaion.sh](mysql-opertaion.s)
在mysql shell中执行sql语句
### bash mysql-opertaion.sh [args] 命令的使用
mysql-opertaion.sh 脚本里封装了几个方法

命令 |   调用的方法  |   说明
------------ | ------------- | -------------
bash mysql-opertaion.sh check-db-talbes-size dbName userName password | check-db-talbes-size [args] |  查看dbName数据库各表容量大小
bash mysql-opertaion.sh check-db-talbe-size tbName dbName userName password | check-db-talbe-size [args] |  查看dbName数据库的tbName表容量大小
