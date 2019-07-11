# 大纲

[第一章 flask的介绍](# 第一章 flask的介绍)

​	[1、app.py.apk中内容介绍](# 1、app.py.apk中内容介绍)

​	[2、app.py中内容介绍](# 2、app.py中内容介绍)

​		[2.1、配置文件](# 2.1、配置文件)

​		[2.2、地址名称、传参](# 2.2、地址名称、传参)



# 第一章 flask的介绍

## 1、app.py.apk中内容介绍

* 模块+静态文件，app = Flask(\_\_name\_\_,.....)

* 路由
  * app.route('/index',methods=['GET'])

* 请求

  * request.form		post请求

  * request.args		get请求

  * request.method	请求方法

* 响应
  * “”		字符串
   * render		模板渲染
   * redirect       重定向	

* session
  * session['xx'] = 123	设置session	
  * session.get('xx')         获取session

## 2、app.py中内容介绍

### 2.1、配置文件

* 配置文件原理

> settings.py

```python
class Foo:
    DEBUG = True
```

> xx.py

```python
import importlib
path = 'settings.Foo'
p,c = path.rsplit('.',maxsplit=1)
m = importlib.import_module(p)
cls = getattr(m,c)
print(cls)      #<class 'settings.Foo'>
#查找类下的内容
for key in dir(cls):
    if key.isupper():
        print(key,getattr(cls,key))
结果：<class 'settings.Foo'>
          DEBUG True
```

* flask 配置

  > app.py

  ```python
  from flask import Flask
  app = Flask(__name__)
  print(app.config)
  # app.config['DEBUG'] = True			#配置方式一
  app.config.from_object("setting.Dev")    #设置配置文件（方式二）
  ```

  > settings.py

  ​	

  ```python
  >>>假设需要在不同场景用不同的配置，可以像如下配置，亦可只配置Dev类实现flask配置
  #共用的配置
  class Base(object):
      xx = 123
  #线上环境
  class Pro(Base):
      DEBUG = False
  #开发环境
  class Dev(object):
      DEBUG = True
  ```

### 2.2、地址名称、传参

> app.py

```python
from flask import Flask, request, url_for
app = Flask(__name__)
app.config.from_object("settings.Dev")



# 请求地址 http://127.0.0.1:5000/index/1/
@app.route('/index/<int:nid>',methods=['GET','POST'],endpoint='n1')
def index(nid):
    print(url_for('n1'))                    # /index/1/
    return 'Index'
```

* app文件包含知识点

  * endpoint	地址的名称，如果不写，默认为函数名
  * /index/1/    传参
    * int类型 	<int: nid>
    * str类型    <nid>
    * .....

  * URL反转
    * url_for	把地址名称反转为url

``