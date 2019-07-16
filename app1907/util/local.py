try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class Local(object):
    __slots__ = ("__storage__", "__ident_func__")       #Loacl对象只能有属性 __storage__、__ident_func__

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



if __name__ == '__main__':


    #实现栈的功能
    obj = Local()   #执行: __init__
    obj.stack = []       #执行 __setattr__


    obj.stack.append('小明')
    obj.stack.append('小米')
    print(obj.stack)            #执行：__getattr__
    print(obj.stack.pop())
    print(obj.stack)
