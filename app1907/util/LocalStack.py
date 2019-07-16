from local import Local
import functools

#__storage__ = { }


#把Local维护成一个栈
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
