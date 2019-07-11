import functools

def auth(func):
    @functools.wraps(func)              #不改变原函数信息（函数名）
    def inner(*args,**kwargs):
        ret = func(*args,**kwargs)
        return ret
    return inner

@auth
def index():
    print('index')


print(index.__name__)


#23
#使用装饰器使用范围，少量函数额外添加功能
#需要大量执行相同的功能，使用