from wtforms import Form
class A(object):
    def __init__(self):
        self.a = 'b'

    def __repr__(self):
        return 'asdfsfd'

a = A()
print(a.__dict__)