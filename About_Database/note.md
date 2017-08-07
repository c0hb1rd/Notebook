# 关系模型
#### 涉及知识点
* `Super Keyword (超级关键字)`：指能唯一标识一个实体（比如数据库中的某条记录）的属性集合
* `Condidate Key (候选关键字)`：不含有多余属性的 `超级关键字`， 假如一个 `超级关键字` 去掉其中任何一个字段后不能再唯一标识一个实体 （记录），则称它为 `候选关键字`
* `Primary Key (主要关键字)`： `候选关键字` 中被选中作为数据唯一标识的键，称为 `主要关键字`
* `Forgein`
* `Prime Attribute (主属性)`：构成 `候选关键字` 的属性集合中的属性
* `Data Element (数据项)`：构成数据的不可分割的最小单位

## 一、Full Functional Dependency (完全函数依赖)
#### 1.1 定义
指在一个关系中，若其中的某个 `非主属性` 的 `数据项` 依赖于这个关系中除它之外的所有属性，则称这个 `非主属性` `完全函数依赖` 于这个关系

#### 1.2 概念
如果一个 `非主属性B函数` 完全依赖于构成某个 `候选关键字` 的一组 `属性集合A` ，而且 `属性集合A` 的任何一个真子集不能被这个 `非主属性B函数` 依赖，则称 `非主属性B函数` `完全函数依赖` 于 `属性集合A`；反之，如果 `非主属性B函数` 能依赖于 `属性集合A` 的真子集，则称 `非主属性B函数` 部分依赖于 `属性集合A`

#### 1.3 举例
##### 1.3.1 地址表关系
* 关系范围：全世界
* 所有属性：`国家`、`省份`、`城市`、`街道`
* 目的：标识一条唯一的街道
* 超级关键字／候选关键字：{`国家`、`省份`、`城市`、`街道`}
* 非主属性：`街道`

##### 1.3.2 依赖
* 真子集 {`国家`、`省份`、`城市`}：成立
* 真子集 {`国家`、`省份`}：不成立
* 真子集 {`省份`、`城市`}：不成立
* 真子集 {`国家`}：不成立
* 真子集 {`城市`}：不成立

##### 1.3.3 结论
`非主属性` `街道` `完全函数依赖`于这个关系（的属性集合）

## 二、待定