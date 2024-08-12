
目录
- [Linux 文件系统](#linux-文件系统)
- [Linux 命令](#linux-命令)
  - [文件处理](#文件处理)
  - [权限管理](#权限管理)
    - [权限属性](#权限属性)
    - [权限用户](#权限用户)
    - [权限组](#权限组)
  - [文件搜索](#文件搜索)
    - [文件路径搜索](#文件路径搜索)
    - [文件内容搜索](#文件内容搜索)
  - [帮助命令](#帮助命令)
  - [压缩与解压缩](#压缩与解压缩)
  - [网络命令](#网络命令)
  - [关机重启](#关机重启)
  - [Vim 编辑器](#Vim-编辑器)
- [软件包](#软件包)
  - [概念](#概念)
  - [RPM-rpm命令](#RPM-rpm命令)
  - [RPM-yum命令](#RPM-yum命令)
- [用户和组管理](#用户和组管理)
  - [用户文件](#用户文件)
    - [用户配置文件](#用户配置文件)
    - [用户管理相关文件](#用户管理相关文件)
  - [用户管理命令](#用户管理命令)
    - [添加用户](#添加用户)
    - [用户密码管理](#用户密码管理)
    - [修改用户信息](#修改用户)
    - [删除用户](#删除用户)
    - [切换用户身份](#切换用户身份)
    - [用户组管理](#用户组管理)
- [权限管理 sudo](#权限管理-sudo)
  - [概念](#概念-1) 
  - [命令](#命令)
- [Shell](#Shell)
  - [概念](#概念-2)
  - [Shell 基础](#Shell-基础)
    - [执行方式](#执行方式)
    - [Bash 基本功能](#Bash-基本功能)
    - [Bash 变量](#Bash-变量)
    - [Bash 数值运算](#数值运算与运算符)
    - [环境变量与配置文件](#环境变量配置文件)
  - [Shell 编程](#Shell-编程)
    - [正则表达式与通配符](#正则表达式与通配符)
    - [字符截取命令](#字符截取命令)
    - [字符处理](#字符处理)
    - [条件判断](#条件判断)




# Linux 文件系统
![Linux 文件系统目录结构](https://www.runoob.com/wp-content/uploads/2014/06/d0c50-linux2bfile2bsystem2bhierarchy.jpg)

```text
- /              # 根目录
- /boot          # 存放用于系统引导（启动）时使用的各种文件
- /root          # 系统管理员目录，系统管理员的主目录
- /home          # 用户主目录，每个用户都有一个自己的目录，一般该目录名是以用户的账号命名的，如上图中的 alice、bob 和 eve。
- /etc           # 系统配置文件,存放所有的系统管理所需要的配置文件和子目录
- /bin           # 存放二进制可执行文件(ls、cat、mkdir等)
- /sbin          # 存放二进制可执行文件，只有root才能访问
- /tmp           # 临时文件目录，存放临时文件
- /run           # 存放临时文件
- /var           # 存放运行时需要改变数据的目录(动态数据)
- /mnt           # 临时挂载点目录，各种设备挂载到系统后，会在/mnt目录下生成相应设备的目录，比如挂载光驱、文件系统、CD等。

- /usr           # 用户软件目录, 存放用户软件，unix shared resources(共享资源)
- /usr/bin       # 存放用户命令
- /usr/sbin      # 存放用户管理命令，超级用户使用的比较高级的管理程序和系统守护程序。
- /usr/lib       # 存放用户命令需要的共享库
- /usr/share     # 存放共享数据
- /usr/local     # 存放软件升级后新的功能存放目录

- /dev           # 用于存放设备文件
- /proc          # 虚拟文件系统，存放系统内存的映射
- /sys           # 虚拟文件系统，存放系统内存的映射
- /lib           # 存放跟文件系统中的程序运行所需要的共享库及内核模块

```

# Linux 命令

## 文件处理
```shell
# 以下为简单的命令，具体可看 bash
clear         # 清空屏幕
ctr + l       # 清屏（快捷键）

env           # 显示环境变量
df -h         # 显示磁盘使用情况
pstree        # 显示进程树
pwd           # 显示当前工作目录
who           # 显示当前登录用户
whoami        # 显示当前用户
```

```shell
ls -l # 列出文件
ls -lR # 列出所有文件(不要轻易用)
ls -lh # 列出文件，以易读的方式显示文件大小
   # 查看到文件权限的时候，第一个字符表示文件权限，后面是文件所有者，后面是文件所属组，后面是文件大小，后面是文件修改时间，后面是文件名
   # 文件类型（文件权限的第一个位置）：- 普通文件，d 目录，l 链接文件，b 块设备文件，c 字符设备文件   
   # 文件权限：r 读权限，w 写权限，x 执行权限，- 没有权限
   # 文件所有者：u 所有者，g 组，o 其他用户
   # 文件所属组：u 所有者，g 组，o 其他用户
ls -la # 列出所有文件，包括隐藏文件
ls -i  # 列出文件，包括文件索引
```

```shell
mkdir <文件路径> # 创建文件夹
mkdir -p <文件路径>  # 递归创建文件夹

rmdir <文件路径> # 删除空白文件夹
rm -r <文件路径> # 删除文件夹
```

```shell
cp <文件路径> <目标路径> # 复制文件
cp -r # 复制目录
cp -p # 保留文件属性
cp -a # 复制文件和目录及其属性
```

```shell
mv <文件路径> <目标路径> # 移动文件
mv <文件路径> <目标路径/新文件名> # 移动并重命名文件
mv <文件> <新文件名> # 当前文件夹下重命名文件
```

```shell
rm -rf  <文件路径> # 删除文件
   -r # 删除目录
   -f # 强制删除   
```
```shell
touch <文件路径> # 创建文件
```
```shell
cat <文件路径> # 显示文件内容
    -n # 显示行号
tac  <文件路径> # 从最后一行开始显示，可以看出 tac 是 cat 的倒着写

head -n <行数> <文件路径> # 显示文件内容，默认显示前10行
tail -n <行数> <文件路径> # 显示文件内容，默认显示后10行
     -f # 跟踪文件变化，当文件内容发生变化时，自动显示变化内容

more <文件路径> # 查看长文件内容，分页显示文件内容，按空格键查看下一页，按 q 键退出

less <文件路径> # 查看长文件内容，分页显示文件内容（可向上翻页），按空格键查看下一页，按 q 键退出，按 / 键搜索，按 n 键搜索下一个
```

```shell
ln <文件路径> <目标路径> # 创建链接文件，硬链接
  -s # 创建软链接，软连接类似windows的快捷方式，文件权限是由软连接指向的文件决定
# 硬链接和软链接的区别：
#    1. 硬链接：文件有多个路径，文件大小不变，不能跨分区。软链接：文件只有一个路径，文件大小不变，可以跨分区
#    2. 硬链接：不能对目录创建硬链接。软链接：可以对目录创建软链接
#    3. 硬链接：删除原文件时，文件不变，类似 cp -p 。软链接：删除原文件时，软链接失效

# 查看是软链接还是硬链接：ls -i 查看文件索引，索引相同，则为硬链接，索引不同，则为软链接
```

## 权限管理
```shell
umask -S # 查看默认权限
umask -S <权限> # 设置默认权限

umask -p # 查看默认权限
umask # 查看默认权限

```
### 权限属性
change mode
```shell
chmod <权限> <文件路径> # 修改文件权限
chmod [{u|g|o|a} {+|-|=} {r|w|x}] <文件或者目录路径>
    # u: 所有者，g: 组，o: 其他用户，a: 所有用户
    # +: 添加权限，-: 删除权限，=: 设置权限
    # r: 读权限，w: 写权限，x: 执行权限
    #    r权限：允许用户查看文件内容，可以列出目录内容
    #    w权限：允许用户修改文件内容，可以创建、删除文件，修改目录
    #    x权限：允许用户执行文件，可以进入目录
    # 例如：chmod u+x,g+w,o+r file.txt    
    # 权限的数字表示： r: 4，w: 2，x: 1
    # 例如： chmod u=rwx,g=rw,o=x file.txt，chmod 761 file.txt
chmod -R <权限> <文件路径> # 递归修改文件权限
```

### 权限用户
change owner
```shell
chown <用户名> <文件路径> # 修改文件所有者
```

### 权限组
change group
```shell
chgrp <组名> <文件路径> # 修改文件所属组
```

## 文件搜索

### 文件路径搜索
```shell
# find 消耗资源大
find <文件路径> <匹配条件>
find <文件路径> -name <文件名> # 搜索文件 *文件名* 模糊搜索
              -iname <文件名> # 搜索文件 忽略大小写
              -size <文件大小> # 搜索文件 文件大小单位：k,M,G,T,P,E,Z. 
              -type <文件类型> # 文件类型：f,d,l,c,b
              -user <用户名> # 搜索文件所属用户
              -group <组名> # 搜索文件所属组
              -inum <索引号> # 搜索文件索引号
```
```shell
locate  <文件名> # 搜索文件 需要先更新locate数据库，如果放在/tmp目录下，一般搜索不到，因为/tmp为临时目录
       -i <文件名> # 忽略大小写
updatedb # 更新locate数据库
```
```shell
which <命令名> # 搜索命令所在路径
whereis <命令名> # 搜索命令所在路径
```

### 文件内容搜索
```shell
grep <关键字> <文件路径> # 搜索文件内容
    -i # 忽略大小写
    -v # 搜索不包含关键字的文件，如忽略注释行：grep -v "^#" file.txt
```

## 帮助命令

```shell
man <命令名 or 配置文件名> # 帮助手册
    1 # 命令帮助
    5 # 配置文件帮助
    
whatis <命令名> # 查看命令,让人知道命令是什么。在root账号下，可以搜索到所有命令
apropos <命令名> # 查看配置
<命令名> --help # 查看shell命令帮助

help <内置命令> # 查看内置命令
```

## 用户管理

```shell
useradd <用户名> # 创建用户
userdel <用户名> # 删除用户
usermod <用户名> # 修改用户
passwd <用户名> # 修改用户密码

who # 查看登录用户信息
w # 查看当前登录用户信息
w <用户名> # 查看当前用户信息
```

## 压缩与解压缩
```shell
gzip <文件名> # 压缩文件，只压缩文件，不压缩目录，
gunzip <文件名> # 解压文件，解压之后，不保留压缩文件

tar -zcvf <压缩文件名: 文件名.tar.gz> <文件名 or 目录名> # 压缩文件
    -z # 打包同时压缩
    -c # 打包
    -v # 显示详细信息
    -f # 指定文件名   
tar -zxvf <压缩文件名: 文件名.tar.gz> <文件名 or 目录名> # 解压文件

zip <压缩文件名: 文件名.zip> <文件名 or 目录名> # 压缩文件，压缩比80%
    -r # 压缩目录
unzip <压缩文件名: 文件名.zip> <文件名 or 目录名> # 解压文件
```

## 网络命令
```shell
white <用户名>
wall <消息> # 发送消息给所有用户

mail <用户名> <消息> # 发送消息给指定用户,ctr + d 保存信息

ping <ip> # 测试主机是否在线
    -c <次数> # 测试次数

ifconfig # 查看网络接口信息
        eth0 
        lo # 本地回环地址

last # 查看登录信息
lastlog # 查看最后一次登录信息

traceroute  # 显示数据包到主机间的路径

netstat # 显示网络统计信息
       -t # 显示TCP连接 
       -u # 显示UDP连接
       -l # 显示监听
       -r # 显示路由表
       -n # 显示IP地址和端口号
       -a # 显示所有连接和监听              
```

## 关机重启
```shell
shutdown -h now # 关机
shutdown -r now # 重启
shutdown -h <时间> # 如shutdown -h 10 , 表示10分钟后关机

halt # 关机
poweroff # 关机
reboot # 重启
init 0 # 关机
   #  0 表示关机
   #  1 表示单用户
   #  2 表示不完全多用户
   #  3 表示完整多用户模式
   #  4 表示未分配
   #  5 表示图形界面
   #  6 表示重启
init 6 # 重启

logout # 退出当前用户
```

## Vim 编辑器
![Vim编辑器工作模式.png](https://www.runoob.com/wp-content/uploads/2014/07/vim-vi-workmodel.png)

![Vim 键盘图.png](https://www.runoob.com/wp-content/uploads/2015/10/vi-vim-cheat-sheet-sch.gif)


# 软件包

Centos 
## 概念
- 源码包
  - 安装速度慢 
  - 可看到源码
  - 性能比二进制包强 5%

- 二进制包（RPM包）
  - 安装速度快 
  - 不可看到源码
  - 依赖性高

## RPM-rpm命令

依赖安装太麻烦

RPM包命令原则：httpd-2.2.15.el6.centos.1.i686.rpm
- httpd       软件包名
- 2.2.15      软件版本
- 15          软件发布次数
- el6.centos  适合的Linux平台
- 1.i686      适合的硬件平台
- rpm         扩展名
 
www.rpmfind.net
```shell
rpm -ivh <软件包> # 安装软件包
rpm -e <软件包> # 卸载软件包

rpm -q <软件包> # 查询软件包是否安装
rpm -qa # 查询所有软件包
rpm -qa | grep httpd # 查询httpd软件包
rpm -qp <软件包> # 查询未安装软件包信息

rpm -V <软件包> # 查看软件包的校验
rpm2cpio <软件包> # 将软件包转换为.cpio格式
cpio -idmv <软件包>.cpio # 将.cpio格式转换为软件包

```

## RPM-yum命令
```shell
yum serch <软件包> # 查询软件包
yum -y install <软件包> # 安装软件包
yum -y update <软件包> # 更新软件包
yum -y remove <软件包> # 卸载软件包 尽量不要卸载系统软件包，因为卸载系统软件包可能会导致系统无法启动

yum list installed # 查询已安装软件包

yum grouplist # 查询软件包组
yum groupinstall "软件包组" # 安装软件包组
```

# 用户和组管理

## 用户文件

### 用户配置文件

用户信息文件
```text
/etc/passwd     # 用户信息
# root:x:0:0:root:/root:/bin/bash
     # 第1字段：用户名
     # 第2字段：密码标志
     # 第3字段：用户ID（UID）
     #   0：超级用户   1-499：系统用户  500+：普通用户   
     # 第4字段：组ID（GID）  分为初始组、附加组
     # 第5字段：用户用户说明
     # 第6字段：用户主目录
     #   普通用户：/home/用户名    系统用户：/root
     # 第7字段：用户默认shell     
```

影子文件（密码文件）
```text
/etc/shadow     # 用户密码信息
# root:*:19683:0:99999:7:::
     # 第1字段：用户名
     # 第2字段：加密密码
     #    如果为 !! 或者 * 表示密码为空，不能登录
     # 第3字段：上一次修改密码的时间
     # 第4字段：密码的最小使用期限
     # 第5字段：密码的最大使用期限
     # 第6字段：密码过期前的警告天数
     # 第7字段：密码过期后的宽限天数
     # 第8字段：密码过期后的账号禁用天数（账号失效时间） 时间戳
     # 第9字段：保留字段         
```
组信息文件
```text
/etc/group      # 组信息
# root:x:0:
     # 第1字段：组名
     # 第2字段：加密密码
     # 第3字段：组ID（GID）
     # 第4字段：组成员列表（附加用户）
```
组密码文件
```text
/etc/gshadow      # 组密码信息
# root:*::
     # 第1字段：组名
     # 第2字段：加密密码
     # 第3字段：组管理员列表（管理员用户名）
     # 第4字段：保留字段（附加用户）
```

### 用户管理相关文件
```text
/root/          # 超级用户主目录，
/home/用户名     # 普通用户主目录

/etc/skel/      # 用户主目录模板文件
```

## 用户管理命令
### 添加用户
```shell
useradd <用户名> # 添加用户
       -d <用户主目录>   # 指定用户主目录
       -g <用户组>     # 指定用户组
       -G <附加用户组>  # 指定附加用户组
       -s <用户登录Shell>  # 指定用户登录Shell, 默认为/bin/bash
       -u <用户UID>     # 指定用户UID
       -m <用户主目录>    # 创建用户主目录

id <用户名> # 查看用户ID信息
       
# 用户默认值文件
/etc/default/useradd   # 查看 `cat /etc/default/useradd`
```
### 用户密码管理
```shell
超级用户
passwd <用户名> # 修改用户密码
       -S   # 查看用户密码状态,仅root用户可执行
       -l   # 锁定用户密码,仅root用户可执行
       -u   # 解锁用户密码,仅root用户可执行

普通用户
passwd   # 修改用户密码，普通用户修改密码要求密码复杂性要求
```
### 修改用户
```shell
usermod <用户名> # 修改用户信息
       -d <用户主目录>   # 指定用户主目录
       -g <用户组>     # 指定用户组
       -u <用户UID>     # 指定用户UID
       -L <用户名>     # 锁定用户密码
       -U <用户名>     # 解锁用户密码
       -s <用户登录Shell>  # 指定用户登录Shell, 默认为/bin/bash
       
change <用户名>  # 修改用户密码状态
       -d <日期>     # 修改用户密码最后一次修改日期
```
### 删除用户
```shell
userdel <用户名> # 删除用户
      -r <用户名>    # 删除用户主目录
```
### 切换用户身份
```shell
id <用户名> # 查看用户ID信息

su <用户名> # 切换用户身份
   -  # 只使用 - 表示带用户的环境变量一起切换（日常操作中需要带这个参数）
   # su - root -c "useradd  <用户名>" : 表示不切换root，用root身份创建用户
   -c <命令>   # 只执行命令，不切换用户身份
```
### 用户组管理
```shell
groupadd <用户组名> # 添加用户组
        -g <用户组ID>    # 指定用户组ID
groupmod <用户组名> # 修改用户组信息
        -g <用户组ID>    # 指定用户组ID
        -n <新用户组名>    # 修改用户组名
groupdel <用户组名> # 删除用户组

gpasswd <用户组名> # 把用户填入组或者从组中删除
       -a <用户名>    # 添加用户到组 
       -d <用户名>    # 从组中删除用户       
```

# 权限管理 sudo

## 概念
sudo 是一个命令，允许用户以root权限运行命令，但是sudo命令本身并不是root用户，而是一个用户，通常为sudo用户。
sudo 操作对象是系统命令，是root将超级用户的权限授予sudo用户，让sudo用户可以执行一些只有root才能执行的系统命令。

`visudo` 文件所在位置：`/etc/sudoers`

## 命令
```shell
sudo -l # 查看sudo权限
audo <命令> # 使用sudo执行命令
```

# Shell

## 概念

Shell 是一个命令语言解释器，它接受用户输入的命令，并将命令传递给操作系统执行。它为用户提供了一个向操作系统发送请求以便运行程序的界面系统。

Shell 是一个强大的编程语言

Shell分类：
- Bourne Shell： sh、ksh、Bash、zsh
- C Shell：csh、tcsh
- Bash

查看本地支持那些Shell：`cat /etc/shells`

## Shell 基础

### 执行方式
[转义字符](https://zh.wikipedia.org/wiki/%E8%BD%AC%E4%B9%89%E5%AD%97%E7%AC%A6)

- **直接执行**
  ```shell
  echo "hello world" # 直接执行
  echo -e '文本' # 里面可以带控制字符、转义字符
  ```
- **脚本执行**

  `vim test.sh`，以下为test.sh的内容，第一行为#!/bin/bash，表示使用/bin/bash来执行脚本，后续可添加对本脚本的解释
  ```shell
  #!/bin/bash
  # Author: xxx
  # Date: 2024-08-08
  # Description: test script
  
  echo "hello world"
  ```
  执行脚本：`bash test.sh`

### Bash 基本功能

**[Bash 脚本常用快捷键](https://www.runoob.com/w3cnote/bash-shortcut.html)**

```shell
history # 查看历史命令
       -c # 清空历史命令
       -w # 保存历史命令到 ~.bash_history
# !字符串：执行历史命令 如果输入的命令是 !ls，则执行最近的ls命令
# !!：执行上一条命令

alias # 查看别名
alias ls='ls -l' # 创建别名
unalias ls # 删除别名
```

```text
# 输入输出
- 标准输入：stdin，文件描述符 0 ，设备文件名 /dev/stdin
- 标准输出：stdout，文件描述符 1 ，设备文件名 /dev/stdout
- 标准错误输出：stderr，文件描述符 2 ，设备文件名 /dev/stderr

# 输出重定向
- 命令 > : 将标准输出重定向到文件
- 命令 >> : 将标准输出以追加的方式重定向到文件
- 错误命令 2> : 将标准错误输出重定向到文件，覆盖
- 错误命令 2>> : 将标准错误输出以追加的方式重定向到文件

# 正确输出和错误输出同时保存
- 命令 > 文件 2>&1 : 将标准输出和标准错误输出都重定向到文件中，覆盖
- 命令 >> 文件 2>&1 : 将标准输出和标准错误输出都重定向到文件中，追加
- 命令 &> 文件 : 将标准输出和标准错误输出都重定向到文件中，覆盖
- 命令 &>> 文件 : 将标准输出和标准错误输出都重定向到文件中，追加
- 命令 >> 文件1 2 >> 文件2 : 将标准输出重定向追加到文件1，将标准错误输出重定向追加到文件2

# 输入重定向
- 命令 < : 将文件作为标准输入，覆盖
```

```text
# 多命令顺序执行
- ; : 命令1;命令2 : 命令1执行完成后，再执行命令2，命令之间没有逻辑关系
- && : 命令1 && 命令2 : 命令1执行成功，再执行命令2，命令1执行失败，命令2不执行（逻辑 与）
- || : 命令1 || 命令2 : 命令1执行失败，才执行命令2，命令1执行成功，命令2不执行（逻辑 或）

# 管道符
- 命令1 | 命令2 : 命令1的正确输出作为命令2的输入
```

```text
# 通配符
- ? : 匹配任意一个字符
- * : 匹配任意多个字符
- [] : 匹配指定范围内的一个字符
- [-] : 匹配指定范围内的任意一个字符
- [^] : 匹配指定范围外的任意一个字符,不是括号中的字符

# 其他特殊字符
- '' : 单引号，表示字符串，不执行任何特殊字符
- "" : 双引号，表示字符串，执行特殊字符
- ` ` : 反引号，表示执行命令，并返回结果，和 $() 类似，但是$()可以嵌套，` `不能嵌套
- $() : 表示执行命令，并将结果返回
- # : 表示注释
- $ : 表示环境变量，调用变量的值。如 $HOME 表示用户家目录，$USER 表示用户名，$PATH 表示环境变量 PATH 的值，$* 表示所有参数，$@ 表示所有参数，$# 表示参数个数，$? 表示上一个命令的退出状态，$! 表示上一个后台命令的进程号，$0 表示脚本名称，$1-$9 表示参数
- \ : 表示转义字符，如 \n 表示换行，\t 表示制表符，\b 表示退格符，\a 表示响铃符，\e 表示转义符，\f 表示换页符，\v 表示垂直制表符，\0 表示空字符，\xhh 表示十六进制字符，\ooo 表示八进制字符，\ddd 表示十进制字符，\x 表示转义字符，\$ 表示转义字符，\` 表示转义字符，\? 表示转义字符，\* 表示转义字符
```

### Bash 变量

- 变量：计算机内存的一个存储区域，用于存储数据
- 变量设置规则：可以由字母、数字、下划线组成，区分大小写，不能以数字开头
  - 变量赋值：变量名=值
  - 变量默认的类型为字符串类型，给变量赋值时，等号左右不能有空格，
  - 变量调用：$变量名
  - 环境变量名称大写，如PATH：表示可执行文件搜索路径
- 变量分类
  - 用户自定义变量：由用户自己定义，变量名只能由字母、数字、下划线组成，区分大小写
  - 环境变量：由系统提供，变量名只能由字母、数字、下划线组成，区分大小写，如 $PATH
  - 位置参数变量：用来向脚本传递参数，变量名不能自定义，作用固定
  - 预定义变量

**用户自定义变量**

只在当前的shell中有效，关闭shell就失效
```shell
变量名=值  # 创建变量
echo $变量名  # 输出变量值
unset 变量名  # 删除变量
set # 列出所有变量
```

**环境变量**

系统变量，全局变量，所有shell都有效
```shell
export 变量名=值  # 创建环境变量
env # 列出所有环境变量
unset 变量名  # 删除环境变量
```

**位置参数变量**
```shell
$0 # 脚本名称
$1-$9 # 传递给脚本的第1-9个参数,10以上的参数用${10}表示
$# # 所有参数个数
$* # 所有参数，所有参数看成一个整体
$@ # 所有参数，每个参数区分对待

# 脚本示例
#!/bin/bash

sum=$(($1+$2))
echo "sum=$sum"
# 执行脚本
chmod 755 test.sh
./test.sh 1 2
```

**预定义变量**
```shell
$? # 上一个命令的退出状态，0表示正常，非0表示异常
$! # 上一个后台命令的进程号
$$ # 当前shell的进程号
```
```shell
read # 读取用户键盘输入
    -p "提示信息"  # 在等read输入时，提示用户输入
    -t 秒数  # 读取用户输入，10秒超时
    -n 字符数 # 读取用户输入，只读取指定字符数  
    -s  # 读取用户输入，不显示输入内容
    -r  # 读取用户输入，不支持回车键   

# 以下为Bash脚本示例
read -p "请输入用户名：" username # 读取用户输入，并提示用户输入
echo "用户名是：$username"

read -t 10 -p "请输入用户名：" username # 读取用户输入，并提示用户输入，10秒超时
echo "用户名是：$username"

read -n 1 -p "请输入用户名：" username # 读取用户输入，并提示用户输入，只读取一个字符
echo "用户名是：$username"

read -s -p "请输入密码：" password # 读取用户输入，并提示用户输入，不显示输入内容
echo "密码是：$password"

read -r -p "是否继续？[y/n]" answer # 读取用户输入，并提示用户输入，不显示输入内容，不支持回车键
if [ "$answer" = "y" ]; then
  echo "继续执行"
  exit 0
  else
  echo "退出"
  exit 1
fi        
```

### 数值运算与运算符

**[Shell 基本运算符](https://www.runoob.com/linux/linux-shell-basic-operators.html)**

```shell
declare [+/-] 变量名=值  # 声明变量，变量名只能由字母、数字、下划线组成，区分大小写
        - : 给变量设置类型属性
        + : 取消变量设置的类型属性
        -i : 整数类型
        -x : 变量声明为环境变量
        -p : 显示指定变量被声明的类型
# 示例
a=1
b=2
declare -i c=$a+$b
echo $c
```

```shell
# expr # 表达式计算
echo $(expr $a + $b)
```
```shell
# $((运算式)) 或 $[运算式]  # 运算
echo $[$a + $b]
echo $(($a + $b))
```

### 环境变量配置文件

具体概念可看[Bash 变量](#bash-变量)
```shell
source <配置文件>  # 读取配置文件，使得修改后的配置文件立即生效

. <配置文件> # 读取配置文件，使得修改后的配置文件立即生效
```
配置文件
```text
- /etc/profile
- /etc/bashrc
- ~/.bash_profile
- ~/.bashrc
- ~/.bash_logout
- ~/.bash_history
```

## Shell 编程
### 正则表达式与通配符
正则表达式用来在文件中匹配符合条件的字符串，正则是包含匹配。`grep`、`awk`、`sed`等命令可以支持正则表达式。

通配符用来匹配符合条件的文件名，通配符是完全匹配。`ls`、`find`、`cp`这些命令不支持正则表达式，所以只能使用`shell`自己的通配符来进行匹配了。
```shell
# 正则表达式

# 示例
cat /etc/passwd | grep "^root" # 匹配以root开头的行
cat /etc/passwd | grep "root$" # 匹配以root结尾的行
cat /etc/passwd | grep "root" # 匹配包含root的行
cat /etc/passwd | grep "root|user" # 匹配包含root或user的行
cat /etc/passwd | grep "root|user" | grep "^root" # 匹配以root开头的包含root或user的行
cat /etc/passwd | grep "root|user" | grep "^root" | grep -v "nologin" # 匹配以root开头的包含root或user的行，并且不包含nologin的行


# 通配符

# 示例
ls /etc/passwd | grep "^root" # 匹配以root
ls /etc/passwd | grep "root$" # 匹配以root结尾
ls /etc/passwd | grep "root" # 匹配包含root的行
ls /etc/passwd | grep "root|user" # 匹配包含root或user的行
ls /etc/passwd | grep "root|user" | grep "^root" # 匹配以root开头的包含root或user的行
```

### 字符截取命令
```shell
cut [选项] <文件名>  # 截取指定字段
    -d 分隔符  # 指定分隔符，默认为制表符
    -f 列号  # 指定截取的列，从1开始
# cut 不能很好的处理空格，所以需要使用awk

# 示例
cut -d ":" -f 1 /etc/passwd # 截取第一列
cut -d ":" -f 1 /etc/passwd | grep "^root" # 截取第一列，并匹配以root开头的行
cut -d ":" -f 1 /etc/passwd | grep "^root" | cut -d ":" -f 1 # 截取第一列，并匹配以root开头的行，再截取第一列
```
```shell
printf "输出类型输出格式" <输出内容>
      %ns    # 输出字符串， n为字符串长度
      %ni    # 输出整数， i为整数的值
      %m.nf  # 输出浮点数， m为整数部分长度， n为小数部分长度
      
# 示例
printf "%-10s %-10s %-10s\n" "姓名" "性别" "年龄"
```
```shell
awk [选项] '{print $1}' <文件名>  # 截取指定字段
    -F 分隔符  # 指定分隔符，默认为制表符
    
# 示例
df -h | awk '{print $1}' # 截取第一列
df -h | awk '{print $1}' | grep "^root" # 截取第一列，并匹配以root开头的行
```
```shell
# sed 是一种几乎包括在所有UNIX平台包括(Linux)的轻量级`流`编辑器。sed主要是用来将数据进行选取、替换、删除、新增的命令
sed [选项] '操作命令' <文件名>  
    -n  # 取消默认的输出，只有被选择的行(默认所有行)才会被输出
    -e '操作命令'  # 多个操作命令，多个命令用分号隔开
    -f '脚本文件'  # 执行脚本文件中的多个操作命令
    -i  # 在原文件上进行修改，不会生成新的文件，如果文件不存在，则创建文件。加后缀可以指定后缀
    
# '操作命令'
    a \  # 在当前行的后面插入内容
    c \  # 替换当前行的内容
    d    # 删除当前行
    i \  # 在当前行的前面插入内容
    p    # 打印当前行
    s '匹配内容' '替换内容'  # 替换当前行的内容，匹配内容可以是正则表达式    
    g    # 将所有匹配到的内容替换为最后一条s命令中的内容        

# 示例
sed -n '2p' /etc/passwd  # 打印第二行
sed -n '2,5p' /etc/passwd  # 打印第二行到第五行
sed '2,5d' /etc/passwd > temp  # 删除第二行到第五行，并将结果保存到temp文件中'
sed 's/root/admin/g' /etc/passwd > temp  # 替换root为admin，并将结果保存到temp文件中'
```

### 字符处理
```shell
sort [选项] <文件名>  # 排序
    -n  # 按数值排序，默认为字符串排序
    -r  # 降序排序
    -k 列号  # 指定排序的列，从1开始
    -t 分隔符  # 指定分隔符，默认为制表符
    -u  # 去重
    -f  # 忽略大小写    
    
# 示例
sort /etc/passwd  # 默认按字符串排序
sort -n /etc/passwd > temp  # 按数值排序，并将结果保存到temp文件中'    
sort -t ":" -k 3,3 /etc/passwd # 按第三列排序     
```

```shell
wc [选项] <文件名>  # 统计行数、单词数、字节数
    -l  # 统计行数
    -w  # 统计单词数
    -m  # 统计字符数
    -c  # 统计字节数

# 示例
wc /etc/passwd  # 统计/etc/passwd文件的行数、单词数、字节数
```

### 条件判断

![文件类型判断.png](images%2Fimg.png)

```shell
# 文件类型判断
- -d  # 判断是否为目录
- -f  # 判断是否为普通文件
- -e  # 判断文件是否存在

# 示例
test -e <文件名>   # 判断文件是否存在
[ -e <文件名> ]     # 判断文件是否存在，在括号两边添加空格
echo $?           # 判断文件是否存在，如果文件存在，返回0，否则返回1
[-d <目录名>] && echo "是目录" || echo "不是目录"   # 判断文件是否为目录
```

![文件权限判断.png](images%2Fimg_1.png)
```shell
# 文件权限判断
- -r  # 判断文件是否可读
- -w  # 判断文件是否可写
- -x  # 判断文件是否可执行

# 示例
[ -r <文件名> ] && echo "可读" || echo "不可读"
```

![文件之间比较.png](images%2Fimg_2.png)
```shell
# 文件之间比较
- -eq  # 判断是否相等
- -ot  # 判断是否不相等
- -ef  # 判断是否为硬链接

# 示例
[ <文件1> -nt <文件2> ] && echo "文件1比文件2新" || echo "文件1不比文件2新
[ <文件1> -ot <文件2> ] && echo "文件1比文件2旧" || echo "文件1不比文件2旧"
[ <文件1> -ef <文件2> ] && echo "文件1和文件2是硬链接" || echo "文件1和文件2不是硬链接"
```

![两数之间的比较.png](images%2Fimg_3.png)
```shell
# 两数之间的比较
- -gt  # 判断是否大于
- -ge  # 判断是否大于等于
- -lt  # 判断是否小于

# 示例
[ <数1> -gt <数2> ] && echo "数1大于数2" || echo "数1不大于数2"
```

![字符串之间的比较.png](images%2Fimg_4.png)
```shell
# 字符串之间的比较
- -z  # 判断字符串是否为空
- -n  # 判断字符串是否不为空

# 示例
[ -z <字符串> ] && echo "字符串为空" || echo "字符串不为空"
name="root"
[ -n $name ] && echo "yes" || echo "no"
aa="12"
bb="23"
[ "$aa" == "$bb"] && echo "yes" || echo "no"  # 注意等号两边要加空格
```

![多重条件判断.png](images%2Fimg_5.png)
```shell
# 多重条件判断
#  示例
aa=23
[ -n "$aa" -a "$aa" -gt 20 ] && echo "yes" || echo "no"

```

### 流程控制
- **if 语句**
  ```shell
  # 单分支条件语句，条件判断式为true时执行程序，条件判断式为false时，不执行任何程序。
  # 注意条件判断式是test 命令，所以条件判断式要加[]，中间要加空格
  if [ 条件判断式 ];then
    程序
  fi
  # 或
  if [ 条件判断式 ]
     then 
       程序
     fi 
  
  # 示例
  #!/bin/bash
  # 统计根分区使用率
  # Author: jensen
  
  root_use=$(df -h | grep "/dev/sdd" | awk '{print $5}' | tr -d "%")
  if [ $root_use -gt 80 ];then
    echo "根分区使用率大于80%"
    echo "请清理根分区"
  fi
  ```
  ```shell
  # 双分支条件语句，条件判断式为true时执行程序，条件判断式为false时，执行else后的程序。
  # 注意条件判断式是test 命令，所以条件判断式要加[]，中间要加空格
  if [ 条件判断式 ];then
    程序
  else
    程序
  fi
  
  # 示例
  #!/bin/bash
  # 数据统计脚本
  # Author: jensen
  
  date=$(date +%Y-%m-%d)
  size=$(du -sh /etc)
  
  if [ -d /tmp/jensen_data ];then
    echo "Date is: $date" > /tmp/jensen_data/ab.txt
    echo "Size is: $size" >> /tmp/jensen_data/db.txt
    cd /tmp/jensen_data
    tar -zcf etc_$date.tar.gz /etc db.txt &> /dev/null
    rm -rf /tmp/jensen_data/db.txt
  else
    mkdir -p /tmp/jensen_data
    echo "Date is: $date" > /tmp/jensen_data/ab.txt
    echo "Size is: $size" >> /tmp/jensen_data/ab.txt
    cd /tmp/jensen_data
    tar -zcf etc_$date.tar.gz /etc ab.txt &> /dev/null
    rm -rf /tmp/jensen_data/ab.txt
  fi          
  ```
  ```shell
  # 多分支条件语句
  if [ 条件判断式1 ];then
    程序1
  elif [ 条件判断式2 ];then
    程序2
  else
    程序,以上所有条件判断式都为false时执行
  fi    
  
  # 示例
  #!/bin/bash
  
  read -p "请输入一个文件名:" file
  
  if [ -z $file ]
  # 判断 file 的值是否为空
     then 
       echo "文件名不能为空,请重新输入"
       exit 1
  elif [ ! -e $file ]
  # 判断 file 的值是否存在
     then
       echo "输入的不是一个文件,请重新输入"
       exit 2
  elif [ -f $file ]
  # 判断 file 的值是否为普通文件
     then
       echo "输入的是一个文件"
  elif [ -d $file ]
  # 判断 file 的值是否为目录
     then
       echo "输入的是一个目录"
  else
    echo "$file 是一个其他类型的文件"
  fi  
  
  chmod 755 test.sh   #  赋予test.sh执行权限
  ./test.sh           #  执行test.sh脚本
  ```

- **case 语句**


