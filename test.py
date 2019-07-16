class Foo(object):
    __slots__ = ('name','age')

    def __init__(self):
        self.a = 'sd'


obj = Foo()
obj.a