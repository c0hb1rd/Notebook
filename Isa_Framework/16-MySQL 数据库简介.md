## MySQL 数据库简介

## 一、实验说明
### 1.1 实验内容
本节主要介绍关系型数据库 `MySQL` 和对它的一些常用操作。

### 1.2 涉及知识点
* `MySQL` 数据库
* `SQL` 查询语言

## 二、什么是数据库
数据库指的是以一定方式储存在一起、能为多个用户共享、具有尽可能小的冗余度、与应用程序彼此独立的数据集合。

## 三、什么是 MySQL
`MySQL` 是一款高性能，成本低和可靠性高，开源且免费的关系型数据库软件，数据集合分为 `库 -> 表 -> 行 -> 列`。通常情况下，一个项目有一个对应的 `库`来存放项目相关数据，这些数据用多张 `表` 分成不同的结构保存，每一 `行` 和 `列` 就形成了 `表` 的结构，而 `关系型` 就体现在 `表` 与 `表` 之间有一定的关联。

不过自从被 `Oracle` 收购之后，免费版本只剩下社区版，而已根据 `Oracle` 的一贯作风，`MySQL` 目前的使用者都会担心它会变成完全付费软件，所以 `MySQL` 的创始人根据 `MySQL` 的基础又开发了 `MariaDB`，一款与 `MySQL` 用法几乎一模一样的数据库软件，目前大部分原先使用 `MySQL` 也逐渐在转向 `MariaDB`。

## 四、结构化查询语言 SQL
### 4.1 概念
`SQL` 是一种语言，一种针对数据库而生，用于对数据库进行操作的语言。

### 4.2 SQL 语言对 MySQL 的常用操作语法
#### 4.2.1 数据库的创建与删除

* 创建默认编码为 `UTF-8` 的数据库
    ```sql
    CREATE DATABASE 数据库名字 DEFAULT CHARACTER SET utf8;
    ```

* 删除数据库
    ``` SQL
    DROP DATABASE 数据库名字;
    ```

* 使用数据库
    ```SQL
    USE 数据库名字;
    ```

#### 4.2.2 数据表的创建与删除
要创建数据表，首先要使用数据库，然后假设我们现在要创建一张有以下三个字段的表
* 姓名
* 年龄
* 性别

而且为了给每一行的数据添加一个唯一的标识供查询做索引，所以还需要一个唯一标识字段，通常为一个约束了主键和自增的整型字段，起始值为整型 1

那么语法是这样子的
```SQL
CREATE TABLE 表名 (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT "唯一标识，约束主键和自增",
    f_name VARCHAR(50) COMMENT "姓名",
    f_age TINTINT COMMENT "年龄",
    f_gender VARCHAR(10) COMMENT "性别"
) CHARSET=utf8;
```

#### 4.2.3 插入数据
向上一张表中插入数据的语法为
```SQL
INSERT INTO 表名(f_name, f_age, f_gender) VALUES('shiyanlou_001', '21', '性别未知');
```

#### 4.2.4 查询数据
* 查询表中所有数据
    ```SQL
    SELECT * FROM 表名;
    ```

* 查询表中指定范围数据，比如1到10行的数据
    ```SQL
    SELECT * FROM 表名 LIMIT 1, 10;
    ```

* 查询表中 id 小于 10 的纪录，也就是前 10 行
    ```SQL
    SELECT * FROM 表名 WHERE id < 10;
    ```

* 查询表中性别为未知性别，年龄小于 22 的数据
    ```SQL
    SELECT * FROM 表名 WHERE f_gender = "未知性别" AND f_age < 22;
    ```

* 查询表中性别为男或者性别为女并且年龄大于 20 的数据
    ```SQL
    SELECT * FROM 表名 WHERE f_gender = "男" OR f_gender = "女" AND f_age > 20;
    ```

#### 4.2.5 删除数据
* 删除所有数据
    ```SQL
    DELETE FROM 表名;
    ```

* 删除指定条件的数据
    ```SQL
    DELETE FROM 表明 WHERE CONDITION_1 = CAUSE_1 AND CONDITION_2 = CAUSE_2, ...;
    ```
#### 4.2.6 修改数据
* 修改每一行数据的性别为未知性别
    ```SQL
    UPDATE 表名 SET f_gender = "未知性别";
    ```

* 修改指定条件成立的数据性别为未知性别
    ```SQL
    UPDATE 表名 SET f_gender = "未知性别" WHERE CONDITION_1 = CAUSE_1 AND CONDITION_2 = CAUSE_2, ...;
    ```

## 五、总结
通过本节我们知道了什么是 `MySQL` 数据库以及 `SQL` 查询语言常用的操作语法。