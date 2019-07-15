
def b():
    print('123')

a = getattr(b,'b',None)

print(type(a))