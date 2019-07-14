from flask import Flask

app = Flask(__name__)



@app.route('/index')
def index():
    return 'Index'


if __name__ == '__main__':
    app.run()
    app.__call__
    app.request_class
    app.session_interface


def __call__(self, environ, start_response):
    #environ    请求相关的所有数据（由wsgi做初步封装）
    #start_response 用于设置相应相关数据
    return self.wsgi_app(environ, start_response)

def wsgi_app(self, environ, start_response):
    """
    request_context()
    #1.获取environ病对其进行再次封装
    #2.从environ中获取名称为session的cookie，解密，反序列化
    #3.两个东西放在“某个神奇”的地方
        """
    ctx = self.request_context(environ)
    #等同于  ctx=RequestContext(self, environ)     self app对象，environ 请求相关的数据
    #ctx.request = Request(environ)
    #self.session = session
    error = None
    try:
        try:
            ctx.push()   #1.将ctx放在‘空调’上，2.执行SecureCookieSessionInterface，去cookie中获取值并给 ctx.session重新赋值
            """
            _request_ctx_stack.push(self)   表示放在‘某个神奇’地方
            
            if self.session is None:
                session_interface = self.app.session_interface
                    》》 session_interface = SecureCookieSessionInterface() 对象
                    》》self.session = 对象.open_session()
                self.session = session_interface.open_session(self.app, self.request)
                                
                if self.session is None:
                    self.session = session_interface.make_null_session(self.app)

            if self.url_adapter is not None:
                self.match_request()
            """

            #4.执行视图函数
            #5.从“某个神奇”获取session，加密，序列化 == =》写cookie
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
        
        6. 把‘某个神奇’的位置清空 
        """
        ctx.auto_pop(error)