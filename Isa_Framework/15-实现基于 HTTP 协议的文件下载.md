## 实习基于 HTTP 协议的文件下载

## 1.1 实验说明
本节主要讲解 `HTTP 协议` 的通信中如何约束客户端把传输的数据保存下来，并为框架实现一个提供文件下载功能的模块。

### 1.2 涉及知识点
* `json` 模块

### 1.3 实验环境
* `Sublimt` 编辑器
* `Python3`
* `Xfce` 终端

### 1.4 实验流程
* 理清 `JSON` 的概念
* 在 `Web 框架中` 实现 `JSON` 模块
* 实战使用这个 `JSON` 模块进行 `API` 开发

## 二、实现 HTTP 文件下载功能
### 2.1 文件下载的原理
通过之前的开发，同学们其实应该也知道了大部分内容比如静态资源，都是把内容从文件中读取之后再返回给客户端，那么如何实现让客户端下载呢？就需要有一个通知，客户端收到这个通知标识，对响应内容就不再去展示，而是保存下来，也就是我们平时在使用的大部分 `Web 应用` 都有提供的下载功能。

### 2.2 HTTP 报头的 Content-Disposition
上一节我们提到了需有有一个通知，让客户端知道这段内容应该是保存下来，那么如何去定义这个通知标识呢？其实 `HTTP 协议` 已经提供了，就是 `Content-Disposition` 参数，它的值可以指定内容为附件类型，并且还可以指定文件名，用法如下
```http
Content-Disposition: attachment; filename="文件名"
```
通过定义为 `attachment` 附件类型，客户端收到响应之后就会自动保存到本地，而文件名如果不定义，则客户端会根据自身的配置判断保存的名字，有的是根据请求的 `URL` 最后路径来作为文件名，有的则是让用户自己定义等。现在我们知道了原理，下一步就来为框架实现文件下载模块吧。

## 三、文件下载模块
其实与通常返回的响应体没什么区别，只是多了 `Content-Disposition` 参数而已，代码如下，定义在框架主体文件中
```python
...

# 返回让客户端保存文件到本地的响应体
def render_file(file_path, file_name=None):

    # 判断服务器是否有该文件，没有则返回 404 错误
    if os.path.exists(file_path):

        # 读取文件内容
        with open(file_path, "rb") as f:
            content = f.read()

        # 如果没有设置文件名，则以 “/” 分割路径取最后一项最为文件名
        if file_name is None:
            file_name = file_path.split("/")[-1]

        # 封装响应报头，指定为附件类型，并定义下载的文件名
        headers = {
            'Content-Disposition': 'attachment; filename="%s"' % file_name
        }

        # 返回响应体
        return Response(content, headers=headers, status=200)
    
    # 如果不存在该文件，返回 404 错误
    return ERROR_MAP['404']
```
模块的逻辑是先判断文件是否存在，如果存在则开始读取文件内容，设置文件名，在响应报文中添加 `Content-Disposition` 参数，最后再返回响应体这样一个流程，下一步就来实战测试一下文件下载吧。


## 四、实战文件下载模块
在 `main.py` 文件中添加一个下载视图，并且绑定到“/downloac"这个 `URL` 上，代码如下
```python
from sylfk import SYLFk, simple_template, redirect, render_json, render_file
...

class Download(BaseView):
    def get(self, request):
        return render_file("main.py")

syl_url_map = [
    ...
    {
        'url': '/download',
        'view': Download,
        'endpoint': 'download'
    }
]
```
运行 `main.py` 之后，再访问“/download”，可以发现浏览器自动下载了一个名为 `main.py` 文件，也就是我们的测试应用主文件 `main.py` 。

至此，文件下载模块也实现完了，整个框架还差最后一个数据库连接模块就可以再实际开发中使用了。

## 总结
这一节我们学会了如何让客户端改变响应内容的展示方式为下载，并且在框架中实现了这个功能模块的封装，至此，整个框架还未实现的模块就只剩下数据库连接模块了，下一章节我们就来了解下 `MySQL` 这个关系型数据库。