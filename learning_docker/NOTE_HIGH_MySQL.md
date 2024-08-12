# 一起学Docker（Part-3）

| List            | SubDirectory                                                 | Description | Notes |
| --------------- | ------------------------------------------------------------ | ----------- | ----- |
| [Mysql](#MYSQL) |                                                              |             |       |
|                 | - [**新建主服务器 3307**](#新建主服务器-3307)<br />- [**新建从服务器 3308**](#新建从服务器-3308) |             |       |



# MYSQL

主从 MySQL 
## 新建主服务器 3307
```shell
docker run --name mysql-master --privileged=true -p 3307:3306 \
-v /mydata/mysql-master/log:/var/log/mysql \
-v /mydata/mysql-master/data:/var/lib/mysql \
-v /mydata/mysql-master/conf:/etc/mysql/conf.d \
-e MYSQL_ROOT_PASSWORD=jensen673 \
-d mysql
# -e MYSQL_DATABASE=test -e MYSQL_USER=test -e MYSQL_PASSWORD=test mysql:5.7
```
my.cnf -> mydata/mysql-master/conf/my.cnf
```text
[mysqld]
## 设置server_id，同一局域网中需要唯一
server_id=101
## 指定不需要同步的数据库名称
binlog-ignore-db=mysql
## 开启二进制日志功能
log-bin=mall-mysql-bin
## 设置二进制日志使用内存大小(事务)
binlog_cache_size=1M
## 设置使用的二进制日志格式(mixed,statement,row)
binlog_format=mixed
## 二进制日志过期清理时间。默认值为0，表示不自动清理。
## expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如:1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
```
重启 容器
```shell
docker restart mysql-master
```
如果遇到容器重启失败，查看容器日志
```shell
docker logs -f mysql-master
```

mysql 数据权限设置
```sql
CREATE USER 'slave'@'%' IDENTIFIED BY 'jensen673';

GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';
[//]: # (grant all privileges on *.* to 'root'@'%' identified by 'jensen673' with grant option;)
```
## 新建从服务器 3308
```shell
docker run --name mysql-slave --privileged=true -p 3308:3306 \
-v /mydata/mysql-slave/log:/var/log/mysql \
-v /mydata/mysql-slave/data:/var/lib/mysql \
-v /mydata/mysql-slave/conf:/etc/mysql/conf.d \
-e MYSQL_ROOT_PASSWORD=jensen673 \
-d mysql
```
my.cnf -> mydata/mysql-slave/conf/my.cnf
```text
[mysqld]
## 设置server_id，同一局域网中需要唯一
server_id=102
## 指定不需要同步的数据库名称
binlog-ignore-db=mysql
## 开启二进制日志功能，以备Slave作为其它数据库实例的Master时使用
log-bin=mall-mysql-slave-bin
## 设置二进制日志使用内存大小(事务)
binlog_cache_size=1M
## 设置使用的二进制日志格式(mixed,statement,row)
binlog_format=mixed
## 二进制日志过期清理时间。默认值为0，表示不自动清理
## expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断
## 如:1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
## relay_log配置中继日志
relay_log=mall-mysql-relay-bin
## log_slave_updates表示slave将复制事件写进自己的二进制日志
log_slave_updates=1
## slave设置为只读(具有super权限的用户除外)
read_only=1
```
重启 容器
```shell
docker restart mysql-slave
```
从主数据库中查看主从同步状态
```sql
show master status;
```



