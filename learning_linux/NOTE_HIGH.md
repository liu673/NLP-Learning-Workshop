
# 一起学Linux（Part-2）



| List            | SubDirectory                                                 | Description | Notes |
| --------------- | ------------------------------------------------------------ | ----------- | ----- |
| [Shell](#Shell) |                                                              |             |       |
|                 | - [**概念**](#概念)                                          |             |       |
|                 | - [**Shell 基础**](#Shell-基础)<br />---- [执行方式](#执行方式)、[Bash 基本功能](#Bash-基本功能)、[Bash 变量](#Bash-变量)<br />---- [数值运算与运算符](#数值运算与运算符)、[环境变量配置文件](#环境变量配置文件) |             |       |
|                 | - [**Shell 编程**](#Shell-编程)<br />---- [正则表达式与通配符](#正则表达式与通配符)、[字符截取命令](#字符截取命令)、[字符处理](#字符处理)<br />---- [条件判断](#条件判断)、[流程控制](#流程控制) |             |       |


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







