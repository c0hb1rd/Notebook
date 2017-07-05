# 表t_admin
## 必须字段
* F_Name
* F_Pwd 记得密码加盐，加盐方法在 `Helper/AuthHelper.py` 中的 `addSalt`
* F_ParentID 超级管理员值为零

