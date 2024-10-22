# MySQL数据类型

MySQL 支持多种类型，大致可以分为三类：**数值、日期/时间和字符串(字符)类型**。

## 数值类型

| 类型         | 大小                                     | 范围（有符号）                                               | 范围（无符号）                                               | 用途            |
| :----------- | :--------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :-------------- |
| TINYINT      | 1 Bytes                                  | (-128，127)                                                  | (0，255)                                                     | 小整数值        |
| SMALLINT     | 2 Bytes                                  | (-32 768，32 767)                                            | (0，65 535)                                                  | 大整数值        |
| MEDIUMINT    | 3 Bytes                                  | (-8 388 608，8 388 607)                                      | (0，16 777 215)                                              | 大整数值        |
| INT或INTEGER | 4 Bytes                                  | (-2 147 483 648，2 147 483 647)                              | (0，4 294 967 295)                                           | 大整数值        |
| BIGINT       | 8 Bytes                                  | (-9,223,372,036,854,775,808，9 223 372 036 854 775 807)      | (0，18 446 744 073 709 551 615)                              | 极大整数值      |
| FLOAT        | 4 Bytes                                  | (-3.402 823 466 E+38，-1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38) | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                  | 单精度 浮点数值 |
| DOUBLE       | 8 Bytes                                  | (-1.797 693 134 862 315 7 E+308，-2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 双精度 浮点数值 |
| DECIMAL      | 对DECIMAL(M,D) ，如果M>D，为M+2否则为D+2 | 依赖于M和D的值                                               | 依赖于M和D的值                                               | 小数值          |

------

## 日期和时间类型

表示时间值的日期和时间类型为DATETIME、DATE、TIMESTAMP、TIME和YEAR。

| 类型      | 大小 ( bytes) | 范围                                                         | 格式                | 用途                     |
| :-------- | :------------ | :----------------------------------------------------------- | :------------------ | :----------------------- |
| DATE      | 3             | 1000-01-01/9999-12-31                                        | YYYY-MM-DD          | 日期值                   |
| TIME      | 3             | '-838:59:59'/'838:59:59'                                     | HH:MM:SS            | 时间值或持续时间         |
| YEAR      | 1             | 1901/2155                                                    | YYYY                | 年份值                   |
| DATETIME  | 8             | '1000-01-01 00:00:00' 到 '9999-12-31 23:59:59'               | YYYY-MM-DD hh:mm:ss | 混合日期和时间值         |
| TIMESTAMP | 4             | '1970-01-01 00:00:01' UTC 到 '2038-01-19 03:14:07' UTC结束时间是第 **2147483647** 秒，北京时间 **2038-1-19 11:14:07**，格林尼治时间 2038年1月19日 凌晨 03:14:07 | YYYY-MM-DD hh:mm:ss | 混合日期和时间值，时间戳 |

------

## 字符串类型

字符串类型指CHAR、VARCHAR、BINARY、VARBINARY、BLOB、TEXT、ENUM和SET。

| 类型       | 大小                  | 用途                            |
| :--------- | :-------------------- | :------------------------------ |
| CHAR       | 0-255 bytes           | 定长字符串                      |
| VARCHAR    | 0-65535 bytes         | 变长字符串                      |
| TINYBLOB   | 0-255 bytes           | 不超过 255 个字符的二进制字符串 |
| TINYTEXT   | 0-255 bytes           | 短文本字符串                    |
| BLOB       | 0-65 535 bytes        | 二进制形式的长文本数据          |
| TEXT       | 0-65 535 bytes        | 长文本数据                      |
| MEDIUMBLOB | 0-16 777 215 bytes    | 二进制形式的中等长度文本数据    |
| MEDIUMTEXT | 0-16 777 215 bytes    | 中等长度文本数据                |
| LONGBLOB   | 0-4 294 967 295 bytes | 二进制形式的极大文本数据        |
| LONGTEXT   | 0-4 294 967 295 bytes | 极大文本数据                    |

>- char(n) 和 varchar(n) 中括号中 n 代表字符的个数，并不代表字节个数，比如 CHAR(30) 就可以存储 30 个字符。
>
>  CHAR 和 VARCHAR 类型类似，但它们保存和检索的方式不同。它们的最大长度和是否尾部空格被保留等方面也不同。在存储或检索过程中不进行大小写转换。
>
>- BINARY 和 VARBINARY 类似于 CHAR 和 VARCHAR，不同的是它们包含二进制字符串而不要非二进制字符串。也就是说，它们包含字节字符串而不是字符字符串。这说明它们没有字符集，并且排序和比较基于列值字节的数值值。
>
>- BLOB 是一个二进制大对象，可以容纳可变数量的数据。有 4 种 BLOB 类型：TINYBLOB、BLOB、MEDIUMBLOB 和 LONGBLOB。它们区别在于可容纳存储范围不同。
>
>-  TEXT 有4种类型：TINYTEXT、TEXT、MEDIUMTEXT 和 LONGTEXT。对应的这 4 种 BLOB 类型，可存储的最大长度不同，可根据实际情况选择。
>
>

-----

# 管理MySQL的命令

## 数据库操作

- **登录数据库**

  ```mysql
  mysql -u root -p
  ```

- **创建数据库**

  ```mysql
  CREATE DATABASE 数据库名;
  create DATABASE RUNOOB;
  # 如果数据不存在则创建，存在则不创建，创建runoob数据库，并设定编码集为utf8
  CREATE DATABASE IF NOT EXISTS RUNOOB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
  ```

- **删除数据库**

  ```mysql
  drop database <数据库名>;
  drop database RUNOOB;
  ```

## 常用命令

- **USE数据库名：**
  选择要操作的Mysql数据库，使用该命令后所有Mysql命令都只针对该数据库

  ```mysql
  use RUNOOB;
  ```

- **SHOW DATABASES:**
  列出 MySQL 数据库管理系统的数据库列表。

  ```mysql
  SHOW DATABASES;
  ```

- **SHOW TABLES:**
  显示指定数据库的所有表，使用该命令前需要使用 use 命令来选择要操作的数据库。

  ```mysql
  use RUNOOB;
  SHOW TABLES;
  ```

- **SHOW COLUMNS FROM *数据表*:**
  显示数据表的属性，属性类型，主键信息 ，是否为 NULL，默认值等其他信息。

  ```mysql
  SHOW COLUMNS FROM runoob_tbl;
  ```

- **SHOW INDEX FROM *数据表*:**
  显示数据表的详细索引信息，包括PRIMARY KEY（主键）。

  ```mysql
  SHOW INDEX FROM runoob_tbl;
  ```

- **SHOW TABLE STATUS [FROM db_name] [LIKE 'pattern'] \G:**
  该命令将输出Mysql数据库管理系统的性能及统计信息。

  ```mysql
  SHOW TABLE STATUS  FROM RUNOOB;   # 显示数据库 RUNOOB 中所有表的信息
  SHOW TABLE STATUS from RUNOOB LIKE 'runoob%';     # 表名以runoob开头的表的信息
  SHOW TABLE STATUS from RUNOOB LIKE 'runoob%'\G;   # 加上 \G，查询结果按列打印
  ```

- ```mysql
  BEGIN;
  ```

- ```mysql
  COMMIT;
  ```

- ```mysql
  DESCRIBE 表名
  ```

| 命令               | 描述                      |
| :----------------- | :------------------------ |
| SELECT VERSION( )  | 服务器版本信息            |
| SELECT DATABASE( ) | 当前数据库名 (或者返回空) |
| SELECT USER( )     | 当前用户名                |
| SHOW STATUS        | 服务器状态                |
| SHOW VARIABLES     | 服务器配置变量            |

## 事务处理

### 4条件

一般来说，事务是必须满足4个条件（ACID）：：原子性（**A**tomicity，或称不可分割性）、一致性（**C**onsistency）、隔离性（**I**solation，又称独立性）、持久性（**D**urability）。

- **原子性：**一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。
- **一致性：**在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。
- **隔离性：**数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。
- **持久性：**事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。

### 处理事务语句

- `BEGIN` 或 `START TRANSACTION `显式地开启一个事务；

- `COMMIT` 也可以使用 `COMMIT WORK`，不过二者是等价的。`COMMIT` 会提交事务，并使已对数据库进行的所有修改成为永久性的；

- `ROLLBACK` 也可以使用` ROLLBACK WORK`，不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；

- `SAVEPOINT identifier`，`SAVEPOINT` 允许在事务中创建一个保存点，一个事务中可以有多个 `SAVEPOINT`；

  savepoint 是在数据库事务处理中实现“子事务”（subtransaction），也称为嵌套事务的方法。事务可以回滚到 savepoint 而不影响 savepoint 创建前的变化, 不需要放弃整个事务。

  ROLLBACK 回滚的用法可以设置保留点 SAVEPOINT，执行多条操作时，回滚到想要的那条语句之前。

  使用 SAVEPOINT
  ```mysql
  SAVEPOINT savepoint_name;    // 声明一个 savepoint
  
  ROLLBACK TO savepoint_name;  // 回滚到savepoint
  ```

  删除 SAVEPOINT

  保留点再事务处理完成（执行一条 ROLLBACK 或 COMMIT）后自动释放。

  MySQL5 以来，可以用:
  ```mysql
  RELEASE SAVEPOINT savepoint_name;  // 删除指定保留点
  ```

  

- `RELEASE SAVEPOINT identifier` 删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常；

- `ROLLBACK TO identifier` 把事务回滚到标记点；

- `SET TRANSACTION` 用来设置事务的隔离级别。`InnoDB` 存储引擎提供事务的隔离级别有`READ UNCOMMITTED`、`READ COMMITTED`、`REPEATABLE READ` 和 `SERIALIZABLE`。

### 处理事务方法

1、用 BEGIN, ROLLBACK, COMMIT来实现

- **BEGIN** 开始一个事务
- **ROLLBACK** 事务回滚
- **COMMIT** 事务确认

2、直接用 SET 来改变 MySQL 的自动提交模式:

- **SET AUTOCOMMIT=0** 禁止自动提交
- **SET AUTOCOMMIT=1** 开启自动提交

```mysql
mysql> use RUNOOB;
Database changed
mysql> CREATE TABLE runoob_transaction_test( id int(5)) engine=innodb;  # 创建数据表
Query OK, 0 rows affected (0.04 sec)
 
mysql> select * from runoob_transaction_test;
Empty set (0.01 sec)
 
mysql> begin;  # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into runoob_transaction_test value(5);
Query OK, 1 rows affected (0.01 sec)
 
mysql> insert into runoob_transaction_test value(6);
Query OK, 1 rows affected (0.00 sec)
 
mysql> commit; # 提交事务
Query OK, 0 rows affected (0.01 sec)
 
mysql>  select * from runoob_transaction_test;
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql> begin;    # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql>  insert into runoob_transaction_test values(7);
Query OK, 1 rows affected (0.00 sec)
 
mysql> rollback;   # 回滚
Query OK, 0 rows affected (0.00 sec)
 
mysql>   select * from runoob_transaction_test;   # 因为回滚所以数据没有插入
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql>
```





## 数据表操作

### 创建数据表

**CREATE TABLE table_name (column_name column_type);**

```mysql
CREATE TABLE IF NOT EXISTS `runoob_tbl`(
   `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 如果你不想字段为 NULL 可以设置字段的属性为 NOT NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
# AUTO_INCREMENT定义列为自增的属性，一般用于主键，数值会自动加1。
# PRIMARY KEY关键字用于定义列为主键。 您可以使用多列来定义主键，列间以逗号分隔。
# ENGINE 设置存储引擎，CHARSET 设置编码。
```

### 删除数据表

**DROP TABLE table_name ;**

```mysql
DROP TABLE table_name ;
```

### **数据表插入数据**

```mysql
SHOW COLUMNS FROM table_name\G;

INSERT INTO table_name 
( field1, field2,...fieldN )
VALUES
( value1, value2,...valueN );

# 插入多条数据
INSERT INTO table_name 
(field1, field2,...fieldN)  
VALUES  
(valueA1,valueA2,...valueAN),(valueB1,valueB2,...valueBN),(valueC1,valueC2,...valueCN)......;
```

### **读取数据表**

```mysql
select * from runoob_tbl;
```

### **查询数据**

#### where子句

**where：**数据库中常用的是where关键字，用于在初始表中筛选查询。它是一个约束声明，用于约束数据，在返回结果集之前起作用。

**group by:**对select查询出来的结果集按照某个字段或者表达式进行分组，获得一组组的集合，然后从每组中取出一个指定字段或者表达式的值。

**having：**用于对where和group by查询出来的分组经行过滤，查出满足条件的分组结果。它是一个过滤声明，是在查询返回结果集以后对查询结果进行的过滤操作。
执行顺序：
`from,including JOINS` --> `where` --> `group by` --> `having` --> `WINDOW functions` --> `select` --> `distinct` --> `union` --> `order by` --> `limit and offset`

- ```mysql
  SELECT column_name,column_name
  FROM table_name
  [WHERE Clause]
  [LIMIT N][ OFFSET M]
  ```

>1. 查询语句中你可以使用一个或者多个表，表之间使用逗号(,)分割，并使用WHERE语句来设定查询条件。
>2. SELECT 命令可以读取一条或者多条记录。
>3. 星号（*）来代替其他字段，SELECT语句会返回表的所有字段数据
>4. 使用 WHERE 语句来包含任何条件。
>5. 使用 LIMIT 属性来设定返回的记录数。
>6. 通过OFFSET指定SELECT语句开始查询的数据偏移量。默认情况下偏移量为0。

- **where子句**		

    - 查询语句中你可以使用一个或者多个表，表之间使用逗号**,** 分割，并使用***WHERE语句来设定查询条件**。*


    >2. 你可以在 WHERE 子句中指定任何条件。
    >3. 你可以使用 AND 或者 OR 指定一个或多个条件。
    >4. WHERE 子句也可以运用于 SQL 的 DELETE 或者 UPDATE 命令
    >5. WHERE 子句类似于程序语言中的 if 条件，根据 MySQL 表中的字段值来读取指定的数据。

    - 使用 ***BINARY 关键字***来设定 WHERE 子句的字符串比较是区分大小写的。
        ```mysql
        SELECT * from runoob_tbl WHERE BINARY runoob_author='runoob.com';
        ```

#### like子句

like匹配/模糊匹配，会与`%`和`_`结合使用

```shell
'%a'     //以a结尾的数据
'a%'     //以a开头的数据
'%a%'    //含有a的数据
'_a_'    //三位且中间字母是a的
'_a'     //两位且结尾字母是a的
'a_'     //两位且开头字母是a的
```



```mysql
SELECT field1, field2,...fieldN 
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'

# 例
SELECT * from runoob_tbl  WHERE runoob_author LIKE '%COM';
```

> - 在 WHERE 子句中指定任何条件。
> - 在 WHERE 子句中使用LIKE子句。
> - 使用LIKE子句代替等号 **=**。
> - LIKE 通常与 **%** 一同使用，类似于一个元字符的搜索。
> - 使用 AND 或者 OR 指定一个或多个条件。
> - 在 DELETE 或 UPDATE 命令中使用 WHERE...LIKE 子句来指定条件。

#### 正则表达式

通过 **LIKE ...%** 来进行模糊匹配

| 模式       | 描述                                                         |
| :--------- | :----------------------------------------------------------- |
| ^          | 匹配输入字符串的开始位置。如果设置了 RegExp 对象的 Multiline 属性，^ 也匹配 '\n' 或 '\r' 之后的位置。 |
| $          | 匹配输入字符串的结束位置。如果设置了RegExp 对象的 Multiline 属性，$ 也匹配 '\n' 或 '\r' 之前的位置。 |
| .          | 匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用像 '[.\n]' 的模式。 |
| [...]      | 字符集合。匹配所包含的任意一个字符。例如， '[abc]' 可以匹配 "plain" 中的 'a'。 |
| [^...]     | 负值字符集合。匹配未包含的任意字符。例如， '[^abc]' 可以匹配 "plain" 中的'p'。 |
| p1\|p2\|p3 | 匹配 p1 或 p2 或 p3。例如，'z\|food' 能匹配 "z" 或 "food"。'(z\|f)ood' 则匹配 "zood" 或 "food"。 |
| *          | 匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,}。 |
| +          | 匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。 |
| {n}        | n 是一个非负整数。匹配确定的 n 次。例如，'o{2}' 不能匹配 "Bob" 中的 'o'，但是能匹配 "food" 中的两个 o。 |
| {n,m}      | m 和 n 均为非负整数，其中n <= m。最少匹配 n 次且最多匹配 m 次 |

```mysql
# 查找name字段中以'st'为开头的所有数据
SELECT name FROM person_tbl WHERE name REGEXP '^st'

#查找name字段中以'ok'为结尾的所有数据
SELECT name FROM person_tbl WHERE name REGEXP 'ok$';

# 查找name字段中包含'mar'字符串的所有数据：
SELECT name FROM person_tbl WHERE name REGEXP 'mar';

# 查找name字段中以元音字符开头或以'ok'字符串结尾的所有数据：
SELECT name FROM person_tbl WHERE name REGEXP '^[aeiou]|ok$';
```



#### 多表查询

在 SELECT, UPDATE 和 DELETE 语句中使用 Mysql 的 JOIN 来联合多表查询。

JOIN 按照功能大致分为如下三类：

- **INNER JOIN（内连接,或等值连接）**：获取两个表中字段匹配关系的记录。(交集)

  ```mysql
  SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a INNER JOIN tcount_tbl b ON a.runoob_author = b.runoob_author;
  
  SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a, tcount_tbl b WHERE a.runoob_author = b.runoob_author;
  ```

  

- **LEFT JOIN（左连接）：**获取左表所有记录，即使右表没有对应匹配的记录。

  ```mysql
  SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a LEFT JOIN tcount_tbl b ON a.runoob_author = b.runoob_author;
  ```

  

- **RIGHT JOIN（右连接）：** 与 LEFT JOIN 相反，用于获取右表所有记录，即使左表没有对应匹配的记录。

  ```mysql
  SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a RIGHT JOIN tcount_tbl b ON a.runoob_author = b.runoob_author
  ```

#### NULL值处理

MySQL提供了三大运算符:

- **IS NULL:** 当列的值是 NULL,此运算符返回 true。
- **IS NOT NULL:** 当列的值不为 NULL, 运算符返回 true。
- **<=>:** 比较操作符（不同于 = 运算符），当比较的的两个值相等或者都为 NULL 时返回 true。

### 更新数据

`uodate`用来修改表中的数据，形如：`update` 表名称`set` 列名称=新值 `where` 更新条件 

```mysql
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]

# 例
UPDATE runoob_tbl SET runoob_title='学习 C++' WHERE runoob_id=3;
```

>- 同时更新一个或多个字段。
>
>- 在 WHERE 子句中指定任何条件。
>
>- 在一个单独表中同时更新数据。

将特定字符串批量修改为其他字符串时，可以用`replace`

```mysql
UPDATE table_name SET field=REPLACE(field, 'old-string', 'new-string') [WHERE Clause]

# 例
UPDATE runoob_tbl SET runoob_title = REPLACE(runoob_title, 'C++', 'Python') where runoob_id = 3;
```

### 修改数据表

**ALTER** 命令用于修改数据库、表和索引等对象的结构

**ALTER** 命令允许你添加、修改或删除数据库对象，并且可以用于更改表的列定义、添加约束、创建和删除索引等操作。

ALTER 命令非常强大，可以在数据库结构发生变化时进行灵活的修改和调整。

#### 修改表结构

```mysql
# 添加新列
ALTER TABLE table_name
ADD column_name data_type;

# 修改列定义
ALTER TABLE table_name
MODIFY column_name new_data_type;

# 修改列名称
ALTER TABLE table_name
CHANGE old_column_name new_column_name data_type;

# 删除列
ALTER TABLE table_name
DROP column_name;
```

#### 添加约束

```mysql
# 添加主键
ALTER TABLE table_name
ADD PRIMARY KEY (column_name);

# 添加外键
ALTER TABLE table_name
ADD FOREIGN KEY (column_name) REFERENCES referenced_table(ref_column_name);

# 添加唯一约束
ALTER TABLE table_name
ADD CONSTRAINT constraint_name UNIQUE (column_name);
```

#### 创建索引

```mysql
# 创建普通索引
ALTER TABLE table_name
ADD INDEX index_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);

# 创建唯一索引
ALTER TABLE table_name
ADD UNIQUE INDEX index_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);

# 删除索引
ALTER TABLE table_name
DROP INDEX index_name;

# 重命名表
ALTER TABLE old_table_name
RENAME TO new_table_name;
```

#### 修改表存储引擎

```mysql
ALTER TABLE table_name ENGINE = new_storage_engine;

# 例
ALTER TABLE testalter_tbl ENGINE = MYISAM;
```

#### 删除、添加或修改字段

```mysql
# 删除  如果数据表只只剩下一个字段则无法使用DROP来删除字段
ALTER TABLE testalter_tbl  DROP i;
# 添加 默认添加到数据表字段末尾
ALTER TABLE testalter_tbl ADD i INT;

ALTER TABLE testalter_tbl ADD i INT FIRST; # 设置位置
ALTER TABLE testalter_tbl DROP i;
ALTER TABLE testalter_tbl ADD i INT AFTER c;
```

#### 修改字段类型及名称

```mysql
ALTER TABLE testalter_tbl MODIFY c CHAR(10);

# 使用change
ALTER TABLE testalter_tbl CHANGE i j BIGINT;
ALTER TABLE testalter_tbl CHANGE j j INT;
```

#### Null值和默认值的影响

```mysql
mysql> ALTER TABLE testalter_tbl 
    -> MODIFY j BIGINT NOT NULL DEFAULT 100;
```

#### 修改字段默认值

```mysql
# 修改字段默认值
ALTER TABLE testalter_tbl ALTER i SET DEFAULT 1000;

#删除字段默认值
ALTER TABLE testalter_tbl ALTER i SET DEFAULT 1000;
```

#### 修改表名

```mysql
ALTER TABLE testalter_tbl RENAME TO alter_tbl;
```

#### 删除外键约束：keyName

```mysql
alter table tableName drop foreign key keyName;
```



### 删除数据

delete，drop，truncate 都有删除表的作用

drop > truncate > delete

```mysql
DELETE FROM table_name [WHERE Clause]
```

>- 没有指定 WHERE 子句，MySQL 表中的所有记录将被删除。
>- 在 WHERE 子句中指定任何条件
>- 在单个表中一次性删除记录。

### 连接子句

UNION 操作符用于连接两个以上的 SELECT 语句的结果组合到一个结果集合中。多个 SELECT 语句会删除重复的数据。

```mysql
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];

SELECT 列名称 FROM 表名称 UNION SELECT 列名称 FROM 表名称 ORDER BY 列名称；
SELECT 列名称 FROM 表名称 UNION ALL SELECT 列名称 FROM 表名称 ORDER BY 列名称；
```

>- **expression1, expression2, ... expression_n**: 要检索的列。
>- **tables:** 要检索的数据表。
>- **WHERE conditions:** 可选， 检索条件。
>- **DISTINCT:** 可选，删除结果集中重复的数据。默认情况下 UNION 操作符已经删除了重复数据，所以 DISTINCT 修饰符对结果没啥影响。
>- **ALL:** 可选，返回所有结果集，包含重复数据。

### 排序

SELECT 语句使用 ORDER BY 子句将查询数据排序后再返回数据

```mysql
SELECT field1, field2,...fieldN FROM table_name1, table_name2...
ORDER BY field1 [ASC [DESC][默认 ASC]], [field2...] [ASC [DESC][默认 ASC]]

# 例
SELECT * from runoob_tbl ORDER BY submission_date ASC;
```

>- 使用任何字段来作为排序的条件，从而返回排序后的查询结果。
>- 设定多个字段来排序。
>- 使用 ASC 或 DESC 关键字来设置查询结果是按升序或降序排列。 默认情况下，它是按升序排列。
>- 添加 WHERE...LIKE 子句来设置条件。

```mysql
# 如果字符集采用的是 gbk(汉字编码字符集)，直接在查询语句后边添加 ORDER BY
SELECT * FROM runoob_tbl ORDER BY runoob_title;

# 如果字符集采用的是 utf8(万国码)，需要先对字段进行转码然后排序
SELECT * FROM runoob_tbl ORDER BY CONVERT(runoob_title using gbk);
```

### 分组

GROUP BY 语句根据一个或多个列对结果集进行分组。

在分组的列上我们可以使用 COUNT, SUM, AVG,等函数。

```mysql
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;

# 例
SELECT name, SUM(signin) as signin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;

SELECT coalesce(name, '总数'), SUM(signin) as signin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;

```

## 索引

索引是一种数据结构，用于加快数据库查询的速度和性能。

索引分单列索引和组合索引：

- 单列索引，即一个索引只包含单个列，一个表可以有多个单列索引。
- 组合索引，即一个索引包含多个列。

### 普通索引

#### 创建索引

使用 **CREATE INDEX** 语句可以创建普通索引。

```mysql
CREATE INDEX index_name
ON table_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);
```

>- `CREATE INDEX`: 用于创建普通索引的关键字。
>- `index_name`: 指定要创建的索引的名称。索引名称在表中必须是唯一的。
>- `table_name`: 指定要在哪个表上创建索引。
>- `(column1, column2, ...)`: 指定要索引的表列名。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
>- `ASC`和`DESC`（可选）: 用于指定索引的排序顺序。默认情况下，索引以升序（ASC）排序。

#### 修改索引

使用 **ALTER TABLE** 命令可以在已有的表中创建索引

ALTER TABLE 允许你修改表的结构，包括添加、修改或删除索引。

```mysql
ALTER TABLE table_name
ADD INDEX index_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);
```

>- `ALTER TABLE`: 用于修改表结构的关键字。
>- `table_name`: 指定要修改的表的名称。
>- `ADD INDEX`: 添加索引的子句。`ADD INDEX`用于创建普通索引。
>- `index_name`: 指定要创建的索引的名称。索引名称在表中必须是唯一的。
>- `(column1, column2, ...)`: 指定要索引的表列名。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
>- `ASC`和`DESC`（可选）: 用于指定索引的排序顺序。默认情况下，索引以升序（ASC）排序。

#### 创建表的时候直接指定

```mysql
CREATE TABLE table_name (
  column1 data_type,
  column2 data_type,
  ...,
  INDEX index_name (column1 [ASC|DESC], column2 [ASC|DESC], ...)
);
```

> - `CREATE TABLE`: 用于创建新表的关键字。
> - `table_name`: 指定要创建的表的名称。
> - `(column1, column2, ...)`: 定义表的列名和数据类型。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
> - `INDEX`: 用于创建普通索引的关键字。
> - `index_name`: 指定要创建的索引的名称。索引名称在表中必须是唯一的。
> - `(column1, column2, ...)`: 指定要索引的表列名。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
> - `ASC`和`DESC`（可选）: 用于指定索引的排序顺序。默认情况下，索引以升序（ASC）排序。

#### 删除索引

使用 **DROP INDEX** 语句来删除索引

```mysql
DROP INDEX index_name ON table_name;
```

> - `DROP INDEX`: 用于删除索引的关键字。
> - `index_name`: 指定要删除的索引的名称。
> - `ON table_name`: 指定要在哪个表上删除索引。

使用 **ALTER TABLE** 语句删除索引

```mysql
ALTER TABLE table_name
DROP INDEX index_name;
```

> - `ALTER TABLE`: 用于修改表结构的关键字。
> - `table_name`: 指定要修改的表的名称。
> - `DROP INDEX`: 用于删除索引的子句。
> - `index_name`: 指定要删除的索引的名称。

### 唯一索引

使用 **CREATE UNIQUE INDEX** 语句来创建唯一索引

唯一索引确保索引中的值是唯一的，不允许有重复值。

#### 创建索引

```mysql
CREATE UNIQUE INDEX index_name
ON table_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);
```

> - `CREATE UNIQUE INDEX`: 用于创建唯一索引的关键字组合。
> - `index_name`: 指定要创建的唯一索引的名称。索引名称在表中必须是唯一的。
> - `table_name`: 指定要在哪个表上创建唯一索引。
> - `(column1, column2, ...)`: 指定要索引的表列名。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
> - `ASC`和`DESC`（可选）: 用于指定索引的排序顺序。默认情况下，索引以升序（ASC）排序。

#### 修改表结构

```mysql
ALTER table table_name ADD CONSTRAINT indexName UNIQUE  (columnName(length));
```

> - `ALTER TABLE`: 用于修改表结构的关键字。
> - `table_name`: 指定要修改的表的名称。
> - `ADD CONSTRAINT`: 这是用于添加约束（包括唯一索引）的关键字。
> - `index_name`: 指定要创建的唯一索引的名称。约束名称在表中必须是唯一的。
> - `UNIQUE (column1, column2, ...)`: 指定要索引的表列名。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
> - `ASC`和`DESC`（可选）: 用于指定索引的排序顺序。默认情况下，索引以升序（ASC）排序。

#### 创建表的时候直接指定

在 **CREATE TABLE** 语句中使用 **UNIQUE** 关键字来创建唯一索引

```mysql
CREATE TABLE table_name (
  column1 data_type,
  column2 data_type,
  ...,
  CONSTRAINT index_name UNIQUE (column1 [ASC|DESC], column2 [ASC|DESC], ...)
);
```

> - `CREATE TABLE`: 用于创建新表的关键字。
> - `table_name`: 指定要创建的表的名称。
> - `(column1, column2, ...)`: 定义表的列名和数据类型。你可以指定一个或多个列作为索引的组合。这些列的数据类型通常是数值、文本或日期。
> - `CONSTRAINT`: 用于添加约束的关键字。
> - `index_name`: 指定要创建的唯一索引的名称。约束名称在表中必须是唯一的。
> - `UNIQUE (column1, column2, ...)`: 指定要索引的表列名。

#### 四种方式添加索引

- **ALTER TABLE tbl_name ADD PRIMARY KEY (column_list)**:该语句添加一个主键，这意味着索引值必须是唯一的，且不能为NULL。
- **ALTER TABLE tbl_name ADD UNIQUE index_name (column_list):** 这条语句创建索引的值必须是唯一的（除了NULL外，NULL可能会出现多次）。
- **ALTER TABLE tbl_name ADD INDEX index_name (column_list):** 添加普通索引，索引值可出现多次。
- **ALTER TABLE tbl_name ADD FULLTEXT index_name (column_list):**该语句指定了索引为 FULLTEXT ，用于全文索引。

## 临时表

临时表在我们需要保存一些临时数据时是非常有用的。临时表只在当前连接可见，当关闭连接时，Mysql会自动删除表并释放所有空间。

```mysql
CREATE TEMPORARY TABLE SalesSummary 
(product_name VARCHAR(50) NOT NULL, total_sales DECIMAL(12,2) NOT NULL DEFAULT 0.00, avg_unit_price DECIMAL(7,2) NOT NULL DEFAULT 0.00, total_units_sold INT UNSIGNED NOT NULL DEFAULT 0);
```

## 复制表

```mysql
// 获取数据表的完整结构
show create table 旧表名;

// 将上面的结果复制后，修改SQL语句的数据表名，并执行SQL语句
create table 新表名 ...

// 克隆数据表数据
insert into 新表明 (filed1, filed2,filed3...) 
select filed1, filed2, filed3... from 旧表名;
```

## 序列增长

**AUTO_INCREMENT**

```mysql
create table new_table
(
id int unsigned not null auto_increment,
primary key (id),
name varchar(10) not null,
date date not null,
origin varchar(30) not null
);
```

**重置序列**

```mysql
ALTER TABLE new_table DROP id;

alter table new_table
add id int unsigned not null auto_increment first,
add primary key (id);
```

**设置序列开始值**

一般情况下序列的开始值为1，但如果你需要指定一个开始值100

```mysql
create table new_table 
(
id int unsigned not null auto_increment,
primary key (id),
name char(30) not null,
date date not null,
origin varchar(30) not null
)engine=innob auto_increment=100 charset=utf8;

// 也可以在表创建成功后，来实现设置序列开始值
alter table new_table auto_increment=100;
```

## mysql重复数据

### 防止重复数据

在 MySQL 数据表中设置指定的字段为 **PRIMARY KEY（主键）** 或者 **UNIQUE（唯一）** 索引来保证数据的唯一性。

```mysql
# 在设置表中字段时，想保证数据不能重复，设置双主键
create table new_table
(
first_name char(20) not null,
last_name char(30) not null,
sex varchar(20),
primary key (first_name, last_name)
);

# 后续在使用insert into 插入数据的时候，就需要保证上面的主键内容不能为空
```

```mysql
# 另一种方法是添加一个UNIQUE索引
create table new_tbl
(
first_name char(29) not null,
last_name char(10) not null,
sex char(6),
unique (first_name, last_name)
);
```

### 统计重复数据

```mysql
select count(*) as repetitions, last_name, first_name
from new_tbl
group by last_name,first_name
having repetitions >1;
```

### 过滤重复数据

```mysql
select distinct last_name,first_name 
from new_table;
```

### 删除重复数据

```mysql
# 第一种方法
CREATE TABLE tmp SELECT last_name, first_name, sex FROM person_tbl  GROUP BY (last_name, first_name, sex);

DROP TABLE person_tbl;

ALTER TABLE tmp RENAME TO person_tbl;
```

```mysql
# 第二种方法
alter ignore table new_table
add primary key (first_name, last_name);
```

# 导出数据







# SQL注入

SQL注入，就是通过把SQL命令插入到Web表单递交或输入域名或页面请求的查询字符串，最终达到欺骗服务器执行恶意的SQL命令。

防止SQL注入，我们需要注意以下几个要点：

> 1.永远不要信任用户的输入。对用户的输入进行校验，可以通过正则表达式，或限制长度；对单引号和 双"-"进行转换等。
>
> 2.永远不要使用动态拼装sql，可以使用参数化的sql或者直接使用存储过程进行数据查询存取。
>
> 3.永远不要使用管理员权限的数据库连接，为每个应用使用单独的权限有限的数据库连接。
>
> 4.不要把机密信息直接存放，加密或者hash掉密码和敏感的信息。
>
> 5.应用的异常信息应该给出尽可能少的提示，最好使用自定义的错误信息对原始错误信息进行包装
>
> 6.sql注入的检测方法一般采取辅助软件或网站平台来检测，软件一般采用sql注入检测工具jsky，网站平台就有亿思网站安全平台检测工具。MDCSOFT SCAN等。采用MDCSOFT-IPS可以有效的防御SQL注入，XSS攻击等。



































































