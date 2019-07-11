
# 第一章 flask的介绍

## 1 app1.py.bak中介绍内容

* 模块+静态文件，app = Flask(__name,.....)

* 路由
  * app.route('/index',methods=['GET'])

* 请求

  * request.form		post请求

  * request.args		get请求

  * request.method	请求方法

* 响应
  * “ ”		字符串
   * render		模板渲染
   * redirect       重定向	

* session
  * session['xx'] = 123	设置session	
  * session.get('xx')         获取session

## 2 app2.py.bak中介绍内容

### 2.1 index()函数的知识点介绍

#### 2.1.1 配置文件

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

#### 2.2 地址名称、传参

> app.py

```python
from flask import Flask, request, url_for
app = Flask(__name__)
app.config.from_object("settings.Dev")



# 请求地址 http://127.0.0.1:5000/index/1/
@app.route('/index/<int:nid>',methods=['GET','POST'],endpoint='n1')
def index(nid):
    print(url_for('n1',nid=1))                    # /index/1/
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

### 2.2 res()函数知识点介绍

> 响应过程中，可定制响应头和响应体，具体通过浏览器查看响应体和F12查看response hears（响应头）

* 响应体
  * return 'test'                                        字符串
  * return jsonify({'key':'value'})            序列化
  * return redirect('/index')                     重定向

* 定制响应头

```python
obj = make_response('test')			#设置响应体
obj.headers['xxx'] = '123'			#设置响应头之一
obj.set_cookie('key','value')		#设置cookie
return	obj
```

## 3 app3.py.bak中介绍内容

> 对下面操作需要把app3文件放置原本位置，并登录 oldboy	123

### 3.1 限制用户访问页面

> 功能：允许登录用户访问页面，禁止非登录用户访问页面

#### 3.1.1 在视图函数判断

> 直接在视图函数上做判断，缺点：每个需要约束用户都需要添加判断代码

```python
@app.route('/index')
def index():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('index.html', stu_dic=STUDENT_DICT)
```

#### 3.1.2 在视图函数添加装饰器

> 装饰器使用范围：少量函数额外添加功能

* **装饰器存在问题**

  > 装饰器中修饰的函数名会被改变，即如果用于修改视图函数，结果所有的视图函数都会相同

  ```
  def inner(*args,**kwargs):        
      ret = func(*args,**kwargs)        
          return ret    
      return inner
  @inner
  def index():    
      print(index.__name__)
      
  index()			#输出函数名称为：	inner
  ```

* **修复同名函数问题**

  > ```python 
  > functools内置函数，功能：不该变原函数信息
  > ```

```python
import functools
def inner(*args,**kwargs): 
    @functools.wraps(func)			#不改变原函数信息（函数名）
    ret = func(*args,**kwargs)        
        return ret    
    return inner
@inner
def index():    
    print(index.__name__)
    
index()			#输出函数名称为：	index
```

* **装饰器实现功能**

  > 在装饰视图函数过程中，涉及一个顺序的问题
  >
  > @app.route()前装饰@auth	无效，
  >
  > 应@auth def index():pass 视为一个整体给@app.route()所装饰 

  ```python
  #装饰器
  def auth(func):
      @functools.wraps(func)              #不改变原函数信息（函数名）
      def inner(*args,**kwargs):
          if not session.get('user'):
              return redirect(url_for('login'))
          ret = func(*args,**kwargs)
          return ret
      return inner
  #视图函数
  @app.route('/index')
  @auth						#装饰器的顺序
  def index():
      return render_template('index.html', stu_dic=STUDENT_DICT)
  ```

#### 3.1.3 before_request装饰器

> 1、before_request 类似中间件，eg：请求---中间件-----响应
>
> 2、对所有视图函数前生效

* **例子讲解**
```python
@app.before_request
def auth_2():
    print('refore_request')
    
@app.route('/index')
def index():
    print('index')
    return render_template('index.html', stu_dic=STUDENT_DICT)

#当127.0.0.1:5000/index 请求时
#结果为
	refore_request
    index
```

* **before_request实现用户限制**

  > 1、因为是对所有视图函数生效，所以在添加before_request限制用户，应当过滤非限制用户的视图函数
  >
  > 2、before_request类似中间件，在请求前执行所有存在@before_request的函数

  ```python
  @app.before_request
  def auth_2():
      if request.path == '/login':
          return None                 #返回None可通过
      if not session.get('user'):
          return redirect(url_for('login'))
      
  @app.route('/index')
  def index():
      return render_template('index.html', stu_dic=STUDENT_DICT)
  ```

  

### 3.2 模板渲染

> 前端的html渲染实现

#### 3.2.1 变量类型、标签、函数的渲染

```python
def func(arg):
    return arg + 1

@app.route('/tpl')
def tpl():
    context = {
        {'key':'value'}
        'users':['longtai','liusong','zhaohuhu'],
        'txt':"<input type='text'>",
        'txt2':Markup("<input type='text'>"),
        'func':func
    }
    return render_template('tpl.html',**context)
```

> tpl.html

```html
    {{ pwd.value }}|{{ key['value']}}|{{key.get('value')}}		<!-对字典的渲染-->
	{{ users.0 }}<br>			<!-对数组的渲染-->
    {{ users[1] }} <br>			<!-对数组的渲染-->
    {{ txt|safe }}<br>			<!-后台标签在前端加载-->
    {{ txt2 }}<br>				<!-后台标签处理并在前端加载-->
    {{ func(5) }}<br>			<!-后台函数的执行-->
```

#### 3.2.2 模板全局变量

> 在全局范围内定义变量，在任何视图函数渲染的html中皆可使用

```python
#模板全局变量
@app.template_global()
def sa(a1,a2):
    return a1+a2

#模板全局变量（可作为模板的if判断条件）
@app.template_filter()
def db(a1,a2,a3):
    return a1+a2+a3
@app.route('/tpl')
def tpl():
    return render_template('tpl.html')
```

> tpl.html

```html
    {{ sa(1,2) }}<br>

    <!-特殊之处可作为if的条件判断：if 1|db(2,3)--> <!-管道符前为第一参数，db（2,3）参数 -->
    {{ 1|db(2,3) }}<br>

    {% if 1|db(2,3) %}
        <div>判读yes</div>
    {% else %}
        <div>判读no</div>
    {% endif %}
```

#### 3.2.3 宏定义		

> 类似python的函数，需要调用才能使用 



> ptl.html

```html
    <h4>宏定义</h4>
    {% macro cc(name,type='text',value='') %}
        <span>1234</span>
        <div>{{ name }}/{{ type }}</div>
    {% endmacro %}
    <h4>执行宏定义</h4>
        {{ cc('n1') }}
```

#### 3.2.4 模块继承

> loyout.py

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{% block content %}

{% endblock %}
</body>
</html>
```


> tpl.html


```html
{% extends 'layout.html' %}

{% block content %}
	<div>
        继承loyout.hmtl模板
	</div>
	{% include('login.html') %}
{% endblock %}
```

#### 3.2.5 session

```python
#当请求刚到来，flask读取cookie中的session对应的值：xsdafgghjklhgfdsa，并讲该值反序列为字典

#当请求结束时，flask会读取内存中的字典的值，进行序列化和加密
```

#### 3.2.6 flush闪现

> 在session中存储一个数据，读取时通过pop将数据移除

```python
from flask import Flask,flash,get_flashed_messages
@app.route('/page1')
def page1():
    flash('临时数据存储')
    # flash('临时数据存储','error)    #根据分类

    return 'Session'

@app.route('/page2')
def page2():
    print(get_flashed_messages())
    # print(get_flashed_messages(category_filter=['error'])) #取得分类内容

    return 'Session'
```

