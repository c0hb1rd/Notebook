## 实现 MySQL 数据库连接模块

## 一、实验说明
### 1.1 实验内容
本节内容主要讲解如何实现一个 MySQL 数据库连接模块。

### 1.2 涉及知识点
* `PyMySQL` 模块

### 1.3 实验环境
* `Python3`
* `Xfce` 终端
* `Sublimt` 编辑器
* `MySQL` 数据库

### 1.4 环境部署
安装 `PyMySQL` 模块
```bash
pip3 install pymysql
```

### 1.5 实验步骤
* 分析数据库模块需求
* 设计模块结构
* 实现数据库模块
* 实战测试数据库模块


## 二、Pymysql 模块简介
`Pymysql` 是 `Python` 中一个数据库连接模块，提供了数据库连接，语句执行等基础功能，我们的 `Web 框架` 中数据模块这一次会用它作为底层类库重新封装一个适应实际开发场景的数据库连接模块。

## 三、使用 Pymysql 实现数据库连接模块
### 3.1 需求分析
依旧是分析数据库常用操作，在实际开发中，大致有这些必须操作，数据库连接、`SQL` 语句执行、存储过程调用和增删改查，而 `Pymysql` 在进行数据库操作中，如果出现异常那么程序就会抛出异常，所以为了防止应用因为一个细节而导致后续的业务逻辑都发生错误就要捕获这些异常，在需要的时候甚至作为反馈信息展示给用户，那么就要有一个数据结构来存储查询过程产生的各种数据供业务逻辑去判断，下一步就来实现它。

### 3.2 封装数据库结果
首先我们需要有一个状态来判断数据库连接模块本次操作是否成功，需要有一个变量来存放成功执行的查询结果，需要一个存储异常信息的地方，需要一个变量存放操作影响的条目数，这个影响条目数量如果是针对查询操作的话，那就是返回查询出来的数据的总行数，那么它的大致结构如下。
* suc
* result
* error
* rows

下面就来封装它，代码如下，定义在 `dbconnector` 包中
```python
# 数据库返回结果对象
class DBResult:
    suc = False     # 执行成功与否
    result = None   # 执行结果，通常是查询结果集，一个 list 嵌套 dict 的结构
    error = None    # 异常信息
    rows = None     # 影响行数

    # 返回结果集合中指定位置的一条数据
    def index_of(self, index):
        # 判断是否执行成功，是的话接着判断 index 是否为整型，是的话最后再判断 index 是否在有效范围内
        if self.suc and isinstance(index, int) and self.rows > index >= -self.rows:
            # 条件都成立，返回对应下标的结果
            return self.result[index]

        return None

    # 返回结果集合中的第一条数据
    def get_first(self):
        return self.index_of(0)

    # 返回结果集合中的最后一条数据
    def get_last(self):
        return self.index_of(-1)

```
除了在上面提到的四个变量，还添加了三个操作查询结果的方法，第一个是根据指定的下标返回对应的数据，后面两个都是在它的基础上实现的获取第一条数据或者最后一条数据。

而为了方便数据库模块的捕获异常实现，这里要实现一个异常捕获的装饰器，代码如下
```python
# 数据库返回结果对象
class DBResult:
    ...

    # 异常捕获装饰器
    @staticmethod
    def capture(func):
        def decorator(*args, **options):
            # 实例化
            ret = DBResult()

            # 捕获异常
            try:
                # 为 DBResult 对象的 rows 和 result 成员赋值
                ret.rows, ret.result = func(*args, **options)
                # 修改执行状态为 True 表示成功
                ret.suc = True
            except Exception as e:
                # 如果捕获到异常，将异常放进 DBResult 对象的 error 属性中
                ret.error = e
            # 返回 DBResult 对象
            return ret
        # 返回 decorator 方法，其实就相当于返回 DBResult 对象
        return decorator 
```
这个装饰器要求装饰的 `func` 函数返回两个值，分别是执行影响的行数和执行结果，所以下一步我们实现数据库模块的时候，对于被这个装饰器装饰的操作方法都需要返回两个值。

最后就是为了方便调试，我这里还实现了一个 `to_dict` 方法，返回四个属性组成的字典，代码如下
```python
# 数据库返回结果对象
class DBResult:
    ...

    # 构造四个属性组成的字典
    def to_dict(self):
        return {
            'suc': self.suc,
            'result': self.result,
            'error': self.error,
            'rows': self.rows
        }
```

### 3.3 实现数据库模块
#### 3.3.1 模块设计
在前面我们分析过实际开发中数据库的常用操作，所以我们这里可以把对数据库的操作抽象为各种方法，然后为被 `DBResult.capture` 装饰器装饰的方法确保有返回影响行数和结果就行，结构代码如下，定义在 `dbconnector` 包中
```python

# 数据库模块
class BaseDB:

    # 实例对象初始化方法
    def __init__(self, user, password, database='', host='127.0.0.1', port=3306, charset='utf8', cursor_class=pymysql.cursors.DictCursor):
        self.user = user                    # 连接用户
        self.password = password            # 连接用户密码
        self.database = database            # 选择的数据库
        self.host = host                    # 主机名，默认 127.0.0.1
        self.port = port                    # 端口号，默认 3306
        self.charset = charset              # 数据库编码，默认 UTF-8
        self.cursor_class = cursor_class    # 数据库游标类型，默认为 DictCursor，返回的每一行数据集都是个字典
        self.conn = self.connect()        # 数据库连接对象

    # 建立连接
    def connect(self):
        pass

    # 断开连接
    def close(self):
        pass

    # SQL 语句执行方法
    def execute(self, sql, params=None):
        pass

    # 插入数据并获取最新插入的数据标识，也就是主键索引 ID 字段
    def insert(self, sql, params=None):
        pass

    # 存储过程调用
    def process(self, func, params=None):
        pass

    # 创建数据库
    def create_db(self, db_name, db_charset='utf8'):
        pass

    # 删除数据库
    def drop_db(self, db_name):
        pass

    # 选择数据库
    def choose_db(self, db_name):
        pass
```
这里需要注意的是 `insert` 方法，在实际开发中，会有一些应用场景需要对刚插入的数据再次进行操作，所以为了方便操作就需要拿到这条刚插入数据的标识，而这个方法就是为了获取这个标识而存在的。

#### 3.3.2 数据库连接与断开
数据库连接就是从 `PyMySQL` 模块中获取数据库连接对象，代码如下
```python
import pymysql

# 数据库模块
class BaseDB:
    ...

    # 建立连接
    def connect(self):
        # 返回一个数据库连接对象
        return pymysql.connect(host=self.host, user=self.user, port=self.port,
                            passwd=self.password, db=self.database,
                            charset=self.charset,
                            cursorclass=self.cursor_class)
    
    # 断开连接
    def close(self):
        # 关闭数据库连接
        self.conn.close()
```
连接数据库其实就是把对应的参数传进去 `pymysql.connect` 方法中获取一个连接对象而已。

#### 3.3.3 SQL 语句的执行
数据查询方法的流程是首先从数据库连接中获取一个游标或者说光标，就是我们在编辑器里字符当前输入位置的那个一闪一闪的“|”，是一个抽象的概念，这里可以理解为一个输入环境，在数据库场景就是一个让你输入 `SQL` 语言的环境，然后把我们要执行的语句传入这个输入环境中执行，再根据 `DBResult` 封装结果进行返回，下面就来看看代码加深理解吧。
```python
...

# 数据库模块
class BaseDB:
    ...

    # 数据操作，增，删，改，查
    @DBResult.capture
    def execute(self, sql, params=None                                   ):
        # 获取数据库连接对象上下文
        with self.conn as cursor:
            # 如果参数不为空并且时 Dict 类型时，把 SQL 语句与参数一起传入 execute 中调用，反之直接调用 exevute

            # 执行语句并获取影响条目数量
            rows = cursor.execute(sql, params) if params and isinstance(params, dict) else cursor.execute(sql)

            # 获取执行结果
            result = cursor.fetchall()

        # 返回影响条目数量和执行结果
        return rows, result

```
这里同学们可能会奇怪为什么要用 `with` 语法，因为 `with` 操作的是上下文，也就是对实现了 `__enter__` 和 `__exit__`  方法的对象，从开始执行之前到结束执行之后，会自己做一些逻辑封装放在这两个方法中，而 `pymysql.connect` 放回的是一个 `Connection` 对象，这个对象的 `__enter__` 返回了一个游标，而在对数据库进行增删改的时候，是需要调用 `commit` 方法提交本次改动的，并且在改动过程中如果出现错误，则需要回滚数据库到改动之前，这又是一个为什么用 `with` 语法的原因了，因为 `__exit__` 方法里面会自动判断操作操作成功与否来执行 `commit` 提交更新或者 `rollback` 回滚到这次执行之前，所以这里才会使用 `with` 这种写法。

然后又因为被 `DBResult.capture` 所装饰，所以返回值有两个，分别是影响条目数量和执行结果。

#### 3.3.4 获取最新插入数据 ID
这个方法其实 `PyMySQL` 已经帮我们实现好了，而它又只针对插入数据，所以为了更加抽象化，这里我把 `insert_id` 方法去掉，结合 `execute` 封装为 `insert` 方法，代码如下
```python
...

# 数据库模块
class BaseDB:
    ...

    # 插入数据并获取最新插入的数据标识，也就是主键索引 ID 字段
    def insert(self, sql, params=None):
        # 获取 SQL 语句执行之后的 DBResult 对象
        ret = self.execute(sql, params)

        # 为 DBResult 对象的 result 属性重新赋值为插入数据的 ID
        ret.result = self.conn.insert_id()

        # 返回 DBResult 对象
        return ret
    ...
```
`insert` 方法的逻辑也恨简单，也就是在内部调用一下 `execute` 方法，再判断成功与否封装 `INSERT ID` 到 `DBResult` 对象的 `result` 属性中而已。

#### 3.3.5 存储过程调用方法
存储过程是一些列的数据库操作封装在一起的逻辑块，可以理解为一个函数，存储过程的名字就是函数名，所以它也会需要参数传递，在 `PyMySQL` 中提供了一个 `callproc` 方法调用存储过程，这里我们就通过把它和 `DBResult` 结合在一起实现一个返回 `DBResult` 对象的存储过程调用方法，代码如下
```python   
...

# 数据库模块
class BaseDB:
    ...

    # 存储过程调用
    @DBResult.capture
    def process(self, func, params=None):
        # 获取数据库连接对象上下文
        with self.conn as cursor:

            # 如果参数不为空并且时 Dict 类型时，把存储过程名与参数一起传入 callproc 中调用，反之直接调用 callproc
            rows = cursor.callproc(func, params) if params and isinstance(params, dict) else cursor.callproc(func)

            # 获取存储过程执行结果
            result = cursor.fetchall()

        return rows, result
    ...
```

#### 3.3.6 选择、创建与删除数据库
对于创建和删除数据库，其实就是提前把对应的 `SQL` 语句封装好，选择数据库则是调用了 `PyMySQL` 的 `select_db` 方法不过加了异常捕获装饰器而已，代码如下
```python
...

# 数据库模块
class BaseDB:
    ...

    # 创建数据库
    def create_db(self, db_name, db_charset='utf8'):
        return self.execute('CREATE DATABASE %s DEFAULT CHARACTER SET %s' % (db_name, db_charset))

    # 删除数据库
    def drop_db(self, db_name):
        return self.execute('DROP DATABASE %s' % db_name)

    # 选择数据库
    @DBResult.capture
    def choose_db(self, db_name):
        # 调用 PyMySQL 的 select_db 方法选择数据库
        self.conn.select_db(db_name)

        # 因为正确执行的话没有影响条数和执行结果，所以返回两个空值 None
        return None, None
```



以上就是我们 `Web 框架` 的数据库模块，虽然简单了点，但是操作数据库是没问题了，下面我们就在实战中学会如何使用这个模块吧。


## 四、实战数据库模块
### 4.1 需求分析
现在我们已经又了数据库模块，那么我们就可以强化一下之前的登录功能，模拟实际开发中与数据库交互的注册与登录功能。

### 4.2 创建数据库和表
在实验楼的在线环境中，`MySQL` 的默认用户名是 `root`，密码则为空，而首次启动应用则需要创建对应的数据库和表，那么我们先来实现这一部分，在之前的 `core` 目录下创建一个 `database.py` 的文件，敲入以下代码再来分析
```python
from sylfk.dbconnector import BaseDB

db_user = 'root'            # 连接用户名
db_passowrd = ''            # 连接密码
db_database = "shiyanlou"   # 数据库库名

# 捕获异常，首次连接因为数据库是不存在的，所以会抛出数据库不存在的异常，捕获之后再到 except 语句块中进行数据库的初始化
try:
    # 获取数据库连接对象并指定了数据库名，如果数据库不存在，抛出异常
    dbconn = BaseDB(db_user, db_passowrd, db_database)
except Exception as e:
    # 获取异常的代码
    code, _ = e.args

    # 如果异常代码为 1049 也就是数据库不存在异常，则开始创建，反之为未知错误，输出信息并退出程序
    if code == 1049:
        # 创建数据表语句
        create_table = \
'''CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    f_name VARCHAR(50) UNIQUE
) CHARSET=utf8'''

        # 获取一个没有指定数据库的连接对象
        dbconn = BaseDB(db_user, db_passowrd)

        # 创建数据库，返回一个 DBResult 对象
        ret = dbconn.create_db(db_database)

        # 如果创建成功，切换到该数据库中，然后开始创建数据表
        if ret.suc:
            # 创建数据库成功，切换到该数据库中
            ret = dbconn.choose_db(db_database)

            # 如果切换成功，开始创建数据表
            if ret.suc:
                # 创建数据表
                ret = dbconn.execute(create_table)
        
        # 如果以上步骤有任何一步出错，则删除数据库回退到创建数据库之前的状态
        if not ret.suc:
            # 删除数据库
            dbconn.drop_db(db_database)
            
            # 输出错误信息并退出
            print(ret.error.args)
            exit()
    else:
        # 输出错误信息并退出
        print(e)
        exit()
```
实现首次使用初始化数据库的逻辑其实就是知道第一次连接数据库肯定会因为数据库不存在抛出异常。。。嗯，然后捕获这个异常判断下是否真的是因为数据库不存在才触发的后，开始创建数据库和数据表，下一次连接由于数据存在就不会再跑到异常处理代码块中了。

### 4.3 实现一个页面模版，用于登陆和注册是公用
把 `template` 目录下创建 `loing.html` 重命名为 `layout.html`，再修改两处代码，如下
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>  <!-- 修改出 1 -->
    <style>
        body {
            text-align: center;
        }
    </style>
</head>
<body>
<form action="" method="post">
    <h1>{{ message }}</h1>  <!-- 修改出 2 -->
    <input type="text" name="user">
    <input type="submit" value="提交">
</form>
</body>
</html>
```

### 4.4 实现注册功能
因为我们现在要与数据库关联，所以注册其实就是把用户提交的信息保存在数据库里而已，反之登陆是从数据库里面读出信息，这里我们先来实现注册，在 `main.py` 文件中创建一个 `Register` 视图，代码如下
```python
...
from core.database import dbconn
...

class Register(BaseView):
    def get(self, request):
        # 收到 GET 请求时通过模版返回一个注册页面
        return simple_template("layout.html", title="注册", message="输入注册用户名")

    def post(self, request):
        # 把用户提交的信息作为参数，执行 SQL 的 INSERT 语句把信息保存到数据库的表中，我这里就是 shiyanlou 数据库中的 user 表里
        ret = dbconn.insert('INSERT INTO user(f_name) VALUES(%(user)s)', request.form)

        # 如果添加成功，则表示注册成功，重定向到登录页面
        if ret.suc:
            return redirect("/login")
        else:
            # 添加失败的话，把错误信息返回方便调试
            return render_json(ret.to_dict())
```

然后把视图与 `URL` 绑定在 `syl_url_map` 中，链接定义为“/register”，代码如下
```python
...

syl_url_map = [
    {
        'url': '/',
        'view': Index,
        'endpoint': 'index'
    },
    {
        'url': '/register',
        'view': Register,
        'endpoint': 'register'
    },
    {
        'url': '/login',
        'view': Login,
        'endpoint': 'test'
    },
    {
        'url': '/logout',
        'view': Logout,
        'endpoint': 'logout'
    }
]
...
```

### 4.5 实现登录功能
登录功能其实就是把原先的 `Login` 视图里的用户 `POST` 过了的数据到数据库中查一下看看有没有匹配的，如果有，把它放到 `Session` 中，如果没有则返回错误信息并返回到登录页面让用户再次登录，代码如下
```python
class Login(BaseView):
    def get(self, request):
        # 从 GET 请求中获取 state 参数，如果不存在则返回用默认值 1
        state = request.args.get('state', "1")

        # 通过模版返回给用户一个登录页面，当 state 不为 1 时，页面信息返回用户名错误或不存在
        return simple_template("layout.html", title="登录", message="输入登录用户名" if state == "1" else "用户名错误或不存在，重新输入")

    def post(self, request):
        # 把用户提交的信息到数据库中进行查询
        ret = dbconn.execute('''SELECT * FROM user WHERE f_name = %(user)s''', request.form)

        # 如果有匹配的结果，说明注册过，反之再次重定向回登录页面，并附带 state=0 过去，通知页面提示登录错误信息
        if ret.rows == 1:
            # 如果有匹配，获取第一条数据的 f_name 字段作为用户名
            user = ret.get_first()['f_name']

            # 把用户名放到 Session 中
            session.push(request, 'user', user)

            # Session 已经可以验证通过，所以重定向到首页
            return redirect("/")
        return redirect("/login?state=0")
```
### 4.6 运行测试
运行程序
```bash
python3 main.py
```

首先访问首页因为没有登录，依旧会被重定向到“/login”页面中

![](res/s_login.png)

但这一次不管输入什么，它都会提示错误，因为我们的数据库目前是空的

![](res/login_f.png)

所以我们去到“/register”这个页面中去注册，这里我注册用户名为“shiyanlou_001”

![](res/register.png)

注册完之后它会重定向到登陆页面，输入刚刚注册的用户名，可以看到能成功访问到首页了

![](res/s_index_r.png)

## 五、总结
通过本节的学习，我们掌握了数据库常用功能封装，并且对数据库操作对象实现了异常捕获处理，为框架实现了数据库连接模块，最后再通过实战模拟登录学会了如何去使用它，自此我们的框架该有的功能模块全都实现完了，如果是认真仔细跟着文档一步一步学到这的同学，对 `Web 框架` 的理解是不是更加深刻了，而且可以说是对 `Web 框架` 的内部工作流程达到熟悉这种程度都不过分，并且每一个实战的案列代码，都是我精心设计过为最后一章节的实战开发做铺垫的，是模拟真实生活中开发场景的流程和，编码时的设计思想都有包含在里面，在最后一章节我会以一个应用作为总结，教同学们在实际开发中如何设计和实现一个高度灵活的架构，以此应对以后工作中瞬息万变的需求，而下一节我们就先来进行框架的善后工作 -- 异常处理。
