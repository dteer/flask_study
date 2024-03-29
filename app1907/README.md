---
typora-root-url: img
---

[TOC]

# 特殊章节（知识点概要）

- 1-5小节主要讲解（可根据需求进行内容回顾）
  - 配置文件
  - 路由
  - 视图：FBV
  - 请求
  - 响应
  - 模板
  - session
  - flash
  - 中间件
  - 特殊装饰器

* 



# 第一章 flask基础介绍

## 1.1 app1.py.bak中介绍内容

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

## 1.2 app2.py.bak中介绍内容

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

#### 2.1.2 地址名称、传参

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

## 1.3 app3.py.bak中介绍内容

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
  import functools
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

## 1.4 app4.py.bak中介绍内容

> 中间件

### 4.1 flask源码入口

> 源码执行流程

```python
1、flask启动
	app = Flsk(__name__)
	app.run()
2、run方法进入源码
	#run方法一直执行到run_simple(),并传递self对象，进入uwsgi死循环，直到请求发生
    try:
        run_simple(host, port, self, **options)
    finally:
        # reset the first request information if the development server
        # reset normally.  This makes it possible to restart the server
        # without reloader and that stuff from an interactive shell.
        self._got_first_request = False
3、请求过来时，会调用函数中的 __call__方法，flask入口
	   def __call__(self, environ, start_response):
           """The WSGI server calls the Flask application object as the
           WSGI application. This calls :meth:`wsgi_app` which can be
           wrapped to applying middleware."""
           return self.wsgi_app(environ, start_response)
```



### 4.2 中间件实现

> flask中间键只能在请求前后添加一些功能，并不能传递参数或return值给视图函数

```python
class Middleware(object):
    def __init__(self,old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def __call__(self, *args, **kwargs):
        print('前')
        ret = self.old_wsgi_app(*args,**kwargs)
        print('后')
        return ret


if __name__ == '__main__':
    app.wsgi_app = Middleware(app.wsgi_app)
    app.run()
```

## 1.5 app5.py.bak中介绍内容

> 特殊装饰器(类似django中间件)

### 5.1 类装饰器

> ```python
> @app.before_request
> @app.after_request
> ```

​	

* 无返回值

```python
@app.before_request
def x1():
    print('before1')

@app.before_request
def xx1():
    print('before2')

@app.after_request
def x2(response):
    print('after1')
    return response

@app.after_request
def xx2(response):
    print('after2')
    return response

@app.route('/index')
def index():
    print('index')
    return 'index'

#当用户请求127.0.0.1:5000/index时，返回的结果
	before1
	before2
	index
	after2
	after1
```

> 通过上边的结果可以观察到 用户在请求时，
>
> 先会执行 @app.before_request, 再执行 视图函数，后执行 @app.after_request

[图片位置：flask_study/app1907/img/1.png]()

![](/home/tang/mnt/F/学习/flask_study/app1907/img/1.png)

* 有返回值

  > 当其中一个@app.before_request 中存在返回值的执行顺序

  

```python
@app.before_request
def x1():
    print('before1')
    return '走'

#对应的后端结果
	before1
	after2
	after1
#对应的前端结果
	走
```

> 通过上边的结果可以观察到 用户在请求时，
>
> 先会执行 @app.before_request, 如果存在return，直接返回前端，再执行 @app.after_request

[图片位置：flask_study/app1907/img/2.png]()


![](/home/tang/mnt/F/学习/flask_study/app1907/img/2.png)

* before_first_request
  * 只在程序启动，第一次请求使用，

### 5.2 模板装饰器

	> template_global		
	>
	> template_filter
	>
	> 在3.2.2中有介绍和使用



### 5.3 错误信息定制装饰器

> app.errorhandler
>
> 当页面响应404,500 等响应码，都可以通过定制信息返回



```python
#该函数作用，当响应码为404，对该页面进行定制并返回
@app.errorhandler(404)
def not_found(arg):
    print(arg)
    return '没找到'
```

# 第二章 flask再探

### 2.1 视图函数

#### 2.1.1 flask源码探索

> 目的：探索@route.app()源码（本质闭包）
>
> 路由系统 + endpoint工作机制



```python
@app.route('/xxx',endpoint=None)
def index():
    return 'index'

#1、通过跳转到app.route()的源码
	def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
   """
   	源码剖析：在路由源码中，先pop取出endpoint，为空设置为None
   			再执行self.add_url_rule()
   				rule = '/xxx'
   				endpoint = None
   				f = index	#视图函数
   				**options	其他参数
   """
```

​		

##### 2.1.1.1 路由系统源码

> 从上述可以得到路由系统的主要实现函数为 self.add_url_rule()
>
> 下文为通过源码，可以了解并改造源码的过程，
>
> 目的：学习查看源码的过程和对源码掌握是否正确

```python
#通过源码进行改造路由系统

def index():
    return 'index'
#方法一
app.add_url_rule('/xxx',None,index)

#方法二
routers = [
    ('/xxx',index)
]
for item in routers:
    app.add_url_rule(item[0],None,item[1])
```

​	

##### 2.1.1.2  endpoint 源码

> 在探 add_url_rule()方法

* endpoint 为None做的处理

```python
#在 add_url_rule方法在一开始中
if endpoint is None:
    endpoint = _endpoint_from_view_func(view_func)
    options["endpoint"] = endpoint
    
#在_endpoint_from_view_func该方法中
def _endpoint_from_view_func(view_func):
    assert view_func is not None, "expected view func if endpoint is not provided."
    return view_func.__name__

"""
从上述可以看到如果endpoint为None，endpoint= 视图函数名
"""
```

* endpoint 不为空做的处理

  ```python
  #在add_url_rule方法中
  self.view_functions = {}
  if view_func is not None:
      old_func = self.view_functions.get(endpoint)
      if old_func is not None and old_func != view_func:
          raise AssertionError(
              "View function mapping is overwriting an "
              "existing endpoint function: %s" % endpoint
          )
          self.view_functions[endpoint] = view_func
         
   """
   view_func是作为add_url_rule中参数，为视图函数名
   在源码中可以看到通过view_functions字典保存{'路由名':'视图函数名'}
   逻辑：先保存旧的key:value
   		如果有新的传进来，通过路由名获取旧的函数名，和新的函数名判断，
   		如果不相等，证明存在两个或两个以上的函数名有相同的路由名
   """
  
  ```

#### 2.1.2 app.route参数

* rule		url 规则

* view_func        视图函数名称

* endpoint=None       名称，用于反向生产url

* methods=None         允许的请求方法   get...

* strict_slashes=None    对url最后的 /  符号是否严格要求

* redirect_to=None          重定向到指定url

* defaults=None               默认值，当url中无参数，视图函数需要参数时使用

* subdomain=None         子域名访问          

  * ```python
    from flask import Flask,request
    
    app = Flask(__name__)
    app.config['SERVER_NAME'] = 'wupeiqi.com:5000'
    
    """
    测试用：在host文件添加信息 
    127.0.0.1 wupeiqi.com
    127.0.0.1 web.wupeiqi.com
    127.0.0.1 admin.wupeiqi.com
    """
    
    #http://admin.wupeiqi.com:5000/
    @app.route('/',subdomain='admin')
    def admin_index():
        return "admin.your-domain.tld"
    
    #http://web.wupeiqi.com:5000/
    @app.route('/',subdomain='web')
    def web_index():
        return "web.your-domain.tld"
    
    #http://xxx.wupeiqi.com:5000/
    @app.route('/dynamic',subdomain='<username>')
    def web_index(username):
        return username + ".your.domain.tld"
    ```


#### 2.1.3 CBV模式

> 对应 app6.py.bak文件中体现

```python

def auth(func):
    @functools.wraps(func)              #不改变原函数信息（函数名）
    def inner(*args,**kwargs):
        ret = func(*args,**kwargs)
        return ret
    return inner



class UserView(views.MethodView):
    methods = ['GET']               #方法过滤
    decorators = [auth]             #添加装饰器
    def get(self, *args, **kwargs):
        return 'GET'

    def post(self, *args, **kwargs):
        return 'POST'


app.add_url_rule('/user', None, UserView.as_view('uuu'))        #添加路由
```



#### 2.1.4 自定制正则路由


> from werkzeug.routing import BaseConverter
>
> 自定制路由需要创建自定制类并继承 BaseConverter类
>
> 详情查看 app7.py.bak



## 2.2 源码探索

> 探究flask入口所做的内容

### 2.2.1 flask入口操作

> 相关的源码探索请查看 源码探索.md

```python
from flask import Flask
app = Flask(__name__)

@app.route('/index')
def index():
    return 'Index'

if __name__ == '__main__':
    app.run()
    
   
源码跳转：
1. 入口
	    def __call__(self, environ, start_response):
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
        return self.wsgi_app(environ, start_response)
2. 执行流程
	    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
            """
            request_context()
            #1.获取environ病对其进行再次封装
            #2.从environ中获取名称为session的cookie，解密，反序列化
            #3.两个东西放在“某个神奇”的地方
        	"""
        error = None
        try:
            try:
                ctx.push()
                #4.执行视图函数
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None    
             """
        	5.从“某个神奇”获取session，加密，序列化 ===》写cookie
        	6. 把‘某个神奇’的位置清空 
        	"""
            ctx.auto_pop(error)
```

## 2.3 蓝图

> 给开发者提供目录结构，具体蓝图模板

* 蓝图

  * 自定义模板、静态文件

  * 某一类url添加前缀   

    *  eg: app.register_blueprint(ac,url_prefix='/account')  

  * 给一类url添加before_request等全局变量，使用范围为该蓝图

    



# 第三章 上下文管理 

## 1、请求上下文

### 1.1、偏函数

> 帮助开发者自动传递参数

```python
#注意函数需要的传参个数
import functools
def index(a1,a2):
    return a1 + a2
new_res = functools.partial(index,42)

print(index(42,1))		#43
print(new_res(1))		#43

```

### 1.2、面向对象

#### 1.2.1 执行父类的方法

> **\_\_mro\_\_ 是继承关系的顺序（注意执行继承类的方法）**

```python
#继承的方法的使用
class Base(object):
    def func(self):
        print('Base.func')

class Foo(Base):
    def func(self):
        #方式一：根据mro的顺序执行方法
        super(Foo,self).func()
        #方式二：主动执行Bose类的方法
        Base.func(self)
        print('Foo.func')
foo = Foo()
foo.func()
print(Foo.__mro__)

#结果：
    Base.func
    Base.func
    Foo.func
    (<class '__main__.Foo_1'>, <class '__main__.Base_1'>, <class 'object'>)

```

#### 1.2.2 super的执行过程

> *关注点：注意在Base类中super(Base, self).func()，*
>
> *为何Base的类为object，但父类中不存在func函数，照样可以执行*
>
> *而定义obj = Base(),	obj.fun()	则报错*

```python
class Base(object):
    def func(self):
        super(Base, self).func()
        print('Base.func')

class Bar(object):

    def func(self):
        print('Base.func')

class Foo(Base,Bar):
    pass

obj = Foo()
obj.func()
print(Foo.__mro__)

#结果：
    Bar.func
    Base.func
    (<class '__main__.Foo'>, <class '__main__.Base'>, <class '__main__.Bar'>, <class 'object'>)

```

####　1.2.3  \_\_getattr\_\_ ,  \_\_settattr\_\_ 易错点

> 原理没够清晰，暂存

```python
class Foo(object):
    def __init__(self):
        self.storage = {}
        object.__setattr__(self,'storage',{})

    def __getattr__(self, item):
        print('get',item)

    def __setattr__(self, key, value):
        # print(key,value)
        print('set',self.storage)


obj = Foo()
obj.xx = 123
```

#### 1.2.4 面向对象中双下划线的特殊方法

  * \_\_call\_\_

    		* flask源码请求入口
        		* django请求入口（WSGIHandler.\_\_call\_\_）

  * \_\_init\_\_

      * 实例化

  * get,set,del  ---attr

    		* \_\_getattr\_\_
      * \_\_setattr\_\_
      * \_\_delattr\_\_
          * flask Local对象

  * \_\_new\_\_

    		* 单例模式
        		* rest framework序列化

* get,set,del ---item

    * _\_setitem\_\_

    * \_\_getitem\_\_

    * \_\_delitem\_\_

        * ```python
          当对象加中括号是，调用对应的特殊方法
          obj = obj()
          obj['item']
          ```

          

  * \_\_dict\_\_

      * api封装返回数据时：BaseResponse

  * \_\_repr\_\_

  * \_\_mro\_\_

      * 父类继承顺序

  * \_\_str\_\_

  * \_\_slot\_\_

      * 允许对象中使用的属性
      * flask 中Local对象中使用

#### 1.2.5 方法和函数

​	

```python
class Foo(object):
    def func(self)
    	pass


#执行方式一
obj = Foo()
obj.func()	#func方法

#执行方式二
obj = Foo()
Foo.func(obj)		#func函数
Foo.func(123)

#验证
from types import FunctionType,MethodType
print(isinstance(obj.func,FunctionType))
```

### 1.3、基于列表的栈

```python
class stack(object):

    def __init__(self):
        self.data = []

    def push(self,val):
        self.data.append(val)

    def pop(self):
        return self.data.pop()

    def top(self):
        return self.data[-1]

_stack = stack()
_stack.push('家')
_stack.push('鱼')

print(_stack.pop())
print(_stack.pop())
#结果：
	鱼
    家
```

### 1.4、flask源码中的local()

> 知识点：1、\_\_slots\_\_ 
>
> ​				2、object.\_\_setattr\_\_(self, "__storage__", {})
>
> ​				3、利用异常做操作
>
> 作用：为每个线程开辟一个空间

```python 
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

class Local(object):
    #Loacl对象只能有属性 __storage__、__ident_func__
    __slots__ = ("__storage__", "__ident_func__")       

    def __init__(self):
        object.__setattr__(self, "__storage__", {})
        object.__setattr__(self, "__ident_func__", get_ident)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    
    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

obj = Local()   #执行: __init__
obj.session = 123       #执行 __setattr__
#__storage__ = {'线程id或协程id':{'session':'123'}}
print(obj.session)      #执行：__getattr__

```

### 1.5、flask源码中的localstack()

> **把Local维护成一个栈**

```python
#__storage__ = { stack:[] }
import Local
class LocalStack(object):

    def __init__(self):
        self._local = Local()

    def push(self, value):
        rv = getattr(self._local, "stack", None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(value)
        return rv


    def pop(self):
        stack = getattr(self._local, "stack", None)
        if stack is None:
            return None

        #当列表中大于1，就会不断移除内容，当等于1,不再执行移除
        elif len(stack) == 1:
            # release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()

    def top(self):
        try:
            return self._local.stack[-1]
        except(ArithmeticError,ImportError):
            return None



obj = LocalStack()
obj.push('小明')
obj.push('小米')

print(obj.pop())
```

### 1.6、flask对上述知识点的应用

> flask源码中的部分应用原理如下

```python
class RequestContext(object):
    def __init__(self):
        self.request = 'XX'
        self.session = 'oo'


_request_ctx_stack = LocalStack()
_request_ctx_stack.push(RequestContext())

def _lookup_req_object(arg):
    ctx = _request_ctx_stack.top()
    return getattr(ctx,arg)


# print(get_request_or_session('request'))
# print(get_request_or_session('session'))


request = functools.partial(_lookup_req_object,'request')
session = functools.partial(_lookup_req_object,'session')

print(request())
print(session())
```

### 1.7、上下文管理流程

>  上下文管理：request ，具体查看图 flask_study/app1907/img/上下文管理流程图.png



![](上下文管理流程图.png)



## 2、app上下文管理



# 第四章 flask_session

> flask 中的session主要通过 SecureCookieSessionInterface类实现

* 具体实现 查看 app8_flask_session原理.py.bak
  * 需要结合flask的源码找到对应的入口（深入）

# 第五章 数据库

> pip install DBUtils
>
> 在使用原生态数据库语句需要使用连接池以及封装定制的sqlhelper（避免重复劳动）


## 5.1 连接池		

```python
from DBUtils.PooledDB import PooledDB, SharedDBConnection
import pymysql

POOL = PooledDB(
    creator=pymysql,  # 使用连接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None代表不限制连接数
    mincached=2,  # 初始化时，连接池中至少创建的空闲链接，0代表不创建
    maxcached=5,  # 连接池最多闲置的连接，0和None不限制
    maxshared=3,  # 链接池中最多共享的连接数量，0和None表示全共享，ps：连接模块默认为1，不生效
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待，True等待
    maxusage=None,  # 一个连接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,  # ping mysql服务端，检查是否服务可用， 0,1,2,3...
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='',
    charset='utf8',
)

def task():
    conn = POOL.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from tb1')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
```

## 5.2 wtforms的应用

> 具体情况 /flask_study/app1907/app/app11_wtforms



## 5.3 python 基础知识点

### 5.3.1 可迭代对象

> form 为什么在前端可以被循环？？？

```python
#可迭代对象
class Foo(object):
	#对象迭代方式一
    def __iter__(self):
        return iter([1,2,3])
class Foo(object):
    #对象迭代方式二
 	def __iter__(self):
        yield 1
        yield 2
        yield 3

obj = Foo()
for item in obj:
    print(item)

#结果：  1
		2
    	3
```



### 5.3.2 类对象由来

> 从现象一到现象四，可以了解到对象通过 \_\_new\_\_创建，而类的最终创建者为type

```python
#现象一
class Foo(object):
    def __new__(cls,*args,**kwargs):
        return 123
obj = Foo()
print(type(obj))
#结果：<class 'int'>

#现象二
class Foo(object):
    pass
obj = Foo()
print(type(obj))
#结果：<class '__main__.Foo'>

#现象三
class Foo(object):
    def __new__(cls,*args,**kwargs):
        cls = super(Foo,cls).__new__(cls,*args,**kwargs)
        return cls
obj = Foo()
print(type(obj))
#结果：<class '__main__.Foo'>


#现象四
class Foo(object):
    def __new__(cls,*args,**kwargs):
        return cls
obj = Foo()
print(type(obj))
#结果：<class 'type'>


```

### 5.3.3 metaclass(高级语法)

>**创建类是先执行type中的 \_\_init\_\_方法**
>
>**当类实例化时，先执行type的 \_\_call\_\_ 方法，\_\_call\_\_方法返回值是实例化对象**
>
>​	**_\_call\_\_内部调用：**
>
>​			**类._\_new\_\_：创建对象**
>
>​			**类._\_init\_\_：对象初始化**

#### 5.3.3.1类的创建

> 从类的创建方式，可以看到类是通过 type创建的

```python
#类创建方式一
class Foo1(object):
    a1 = 123
    def func(self):
        return 666
obj = Foo()
print(obj.func())
#结果：666

#类创建方式二
Foo2 = type('Foo',(object,),{'a1':123,'func':lambda self:666})
obj = Foo()
print(obj.func())
#结果：666
```

#### 5.3.3.2 自定义type

> 核心点：metaclass指定当前类由谁来创建（默认由type创建）

```python
#类创建方式一
class MyType(type):
    pass
class Foo(object,metaclass=MyType):
    def func(self):
        return 666
obj = Foo()
print(obj)
#结果：<__main__.Foo object at 0x7f3ffab53ac8>

#类创建方式二
Foo = MyType('Foo',(object,),{'a1':123,'func':lambda self:666})
#结果：<__main__.Foo object at 0x7fcd53053b38>
```

#### 5.3.3.3 type的执行流程

> **类实例化前执行type的\_\_init\_\_ 方法**

```python
#注意类Foo没有实例化，并输出了结果：555
class MyType(type):
    def __init__(self,*args,**kwargs):
        super(MyType,self).__init__(*args,**kwargs)
        print('555')

class Foo(object,metaclass=MyType):
    def func(self):
        return 666
   
#结果：555
```



> **类实例化后执行type的_\_call\_\_ 方法**

* 注意打印的顺序

```python
#类Foo实例化后，调用过程
class MyType(type):
    def __init__(self,*args,**kwargs):
        super(MyType,self).__init__(*args,**kwargs)
        print(555)

    #cls代指Foo类
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls,*args,**kwargs)
        cls.__init__(obj)
        print(666)
        return obj

class Foo(object,metaclass=MyType):
    def func(self):
        print(777)

print('444')
obj = Foo()
obj.func()
#结果：  555
		444
		666
    	777
```

## 5.4 wtforms 源码剖析

> 具体请看 /flask_study/app1907/源码探索.md

## 5.4.1 form顺序执行字段的简略版

> 关注点：第一二部分     》》》》name = simple.StringField()

```python
class Base(object):
    num = 0
    def __init__(self, field_class, *args, **kwargs):
        Base.num += 1
        #第二部分
        self.num = Base.num
class A(object):
    a = 1
    def __new__(cls, *args, **kwargs):
        #第一部分
        return Base(cls, *args, **kwargs)
class B(A):
    pass
class C(A):
    pass

a = B()
print(a.num,type(a))
b = C()
print(b.num,type(b))

#结果： 1 <class '__main__.Base'>
		2 <class '__main__.Base'>
```

