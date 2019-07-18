
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


obj = Foo()
obj.func()