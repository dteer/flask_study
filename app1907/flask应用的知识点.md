# 1、 _\_call\_\_

> flask 的程序入口

```python
1、flask中把 app = Flask(__name__) 中的app对象传入 werkzeug（uwsgi包）
    from werkzeug.serving import run_simple
    try:
        run_simple(host, port, self, **options)
2、uwsgi监听客户端，当客户端发起请求，run_simple执行任务
	找到对应的源码位置，可以看到app()执行，即会调用app类中__call__内容
    def execute(app):
        application_iter = app(environ, start_response)

```



# 2、生成器

> 端口选择，存在多端口，选择不为空且存在优先级别较高的一个

```python
_host = "127.0.0.1"
_port = 5000
server_name = self.config.get("SERVER_NAME")
sn_host, sn_port = None, None

if server_name:
    sn_host, _, sn_port = server_name.partition(":")
    host = host or sn_host or _host
    #利用生成器选择最佳端口，port ==》 sn_port ===》 _port
    port = int(next((p for p in (port, sn_port) if p is not None), _port))
```

# 3 、\_\_getattr\_\_ ,_\_setattr\_\_

> 上下文管理器，多线程的数据独享



```python

```

