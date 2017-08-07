## 使用 Werkzeug 实现 WSGI 入口

## 一、实验说明
### 1.1 实验内容
继上一节创建完结构目录后，这一节我们就来进行 `WSGI` 入口的代码实现

### 1.2 涉及知识点
* `WSGI`
* `Werkzeug`

### 1.3 实验环境
* `Python3`
* `sublimt` 编辑器
* `Xfce` 终端

### 1.4 环境部署
```bash
sudo pip3 install werkzeug
```

### 1.5 实验流程
* 建立框架主体
* 实现 `WSGI` 入口适配器
* 导入到框架中并运行

## 二、Werkzeug 模块简介
`Werkzeug` 官方的定义是一个 `WSGI` 工具包，用来作为 `Web 框架` 的底层库，方便开发者用它来实现一个 `Web 框架`，因为它内部已经帮我们实现了从服务器获取的请求和对响应的封装，所以我们可以用它来实现我们的 `Web 框架入口`。

## 三、建立框架主体
框架主体里的代码目前非常简单，因为一开始我们的目的只有一个就是让它跑起来，我们先看下代码再一步一步分析
```python
# 我这里已实验楼名字缩写命名框架名字： “实验楼 Framework”
class SYLFk:            

    # 实例化方法
    def __init__(self):   
        pass

    # 路由追踪，应用请求处理函数调度入口
    def dispatch_request(self):
        pass

    # 启动入口
    def run(self):            
        pass

    # 框架被 WSGI 调用入口的方法
    def __call__(self):       
        pass
```

这里我们可以先看 `run` 方法，这是使用框架实现应用后，应用启动的入口方法，所以我们先来实现它

```python
from werkzeug.serving import run_simple
...

    # 实例化方法
    def __init__(self):
        self.host = '127.0.0.1' # 默认主机
        self.port = 8086  # 默认端口
...
    # 启动入口
    def run(self, **options):
        # 如果有参数进来且值不为空，则赋值
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)

        # 把框架本身也就是应用本身和其它几个配置参数传给 werkzeug 的 run_simple
        run_simple(hostname=self.host, port=self.port, application=self, **options)
...
```
我们的 `run` 方法现在也是还很简单，只是做了初始化工作和启动服务这两件事，最后可以看到把框架本身传给了 `run_simple`，所以下一步我们需要实现框架的 `__call__` 方法。

## 四、实现 WSGI 入口
在实现 `__call__` 方法之前，我们需要先实现 `WSGI` 入口，打开 `wsgi_adapter` 目录下的 __init__.py 文件，敲入下面的代码

```python
from werkzeug.wrappers import Request

# WSGI 调度框架入口
def wsgi_app(app, environ, start_response):
    """
      第一个参数是应用
      第二个参数就是服务器传过来的请求
      第三个参数则是响应载体，这个参数我们完全不会使用到，只需要连同处理结果一起传回给服务器就行
    """
    
    # 解析请求头
    request = Request(environ)
    
    # 把请求传给框架的路由进行处理，并获取处理结果
    response = app.dispatch_request(request)
    
    # 返回给服务器
    return response(environ, start_response)
```
`WSGI` 入口其实很简单，因为大部分工作 `werkzeug` 已经帮我们做好了，我们只需要在获取请求和返回响应之间，把逻辑交由框架去处理而已

接下来我们回到框架主体文件，实现 `__call__` 和 `dispatch_request` 这两个方法

```python
from werkzeug.wrappers import Response

from sylfk.wsgi_adapter import wsig_app
...

    # URL 路由
    def dispatch_request(self, request):
        status = 200  # HTTP状态码定义为 200，表示请求成功

        # 定义响应报头的 Server 属性
        headers = {
          'Server': 'Shiyanlou Framework'
        }

        # 回传实现 WSGI 规范的响应体给 WSGI 模块
        return Response('<h1>Hello, Framework</h1>', content_type='text/html', headers=headers, status=status)
...

    # 框架被 WSGI 调用入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)

```

## 五、启动服务
接下来我们在框架同级目录下建立一个 `main.py` 文件，敲入一下代码
```python
from sylfk import SYLFk


app = SYLFk()
app.run()
```

运行
```bash
python3 main.py
```

然后在浏览器中输入 `http://127.0.0.1:8086` 可以看到页面返回了路由方法中的结果，也就是 “`<h1>Hello，Framework</h1>`”，这里细心的同学可能会发现，不管 `URL` 路径是什么，都会返回同一个页面，这是因为我们的路由里面只有一个结果，下一节我们就来实现真正的路由做到不同的 `URL` 路径返回不同的结果。
![](res/0601.png)

至此，我们的框架初步建立完成。

## 总结
本节内容我们学会了如何使用 `Werkzeug` 实现一个最基本的可运行的框架主体。
