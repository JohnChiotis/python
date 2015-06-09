# Basic decorator
def first_decorator(func):
    def wrap(*a, **k):
        return'%s decorated by first' % func(*a, **k)
    return wrap

@first_decorator
def first_function(msg):
    return "message %s from first function" % (msg)


# Argument receiving style decorators
def second_decorator(stars_print):
    def inner(func):
        def wrap(*a, **k):
            srs = stars_print * '*'
            return'%s %s decorated by second %s' % (srs, func(*a, **k), srs)
        return wrap
    return inner

@second_decorator(3)
def second_function(msg):
    return "message %s from second function" % (msg)


# Class style decorators
class ThirdDecorator(object):
    def __init__(self, message=None):
        self._message = message
        
    def __call__(self, func):
        def wrap(*a, **k):
            return'%s decorated by %s' % (func(*a, **k), self._message)
        return wrap

@ThirdDecorator(message='THIRD')
def third_function(msg):
    return "message %s from third function" % (msg)


if __name__ == '__main__':
    print first_function('msg_one')
    print second_function('msg_two')
    print third_function('msg_three')
