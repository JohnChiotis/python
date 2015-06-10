# import abc

class MyAbstractMeta(type):
    abstract_items = set()
    def __new__(cls, *a, **k):
        if a[2].get('__metaclass__') == MyAbstractMeta:
            for attr in a[2]:
                if hasattr(a[2][attr], '__abstract__'):
                    cls.abstract_items.add(attr)
        else:
            for method in cls.abstract_items:
                if a[2].get(method) == None:
                    raise NotImplementedError("%s: %s not implemented!" %\
                                             (a[0], method))
        return type.__new__(cls, *a, **k)

    def __init__(self, *a, **k):
        super(MyAbstractMeta, self).__init__(*a, **k)


def my_abstract_method_decorator(f):
    def wrap(*a, **k):
        return f(*a, **k)
    wrap.__abstract__ = True
    return wrap


class MyAbstractClass(object):
    # __metaclass__ = abc.ABCMeta
    __metaclass__ = MyAbstractMeta

    # @abc.abstractmethod
    @my_abstract_method_decorator
    def my_abstract_method(self):
        pass


class SubclassOne(MyAbstractClass):
    def my_abstract_method(self):
       return 'Hi!'


class SubclassTwo(MyAbstractClass):
    pass


if __name__ == '__main__':
    for definition in (SubclassOne, SubclassTwo):
        sub = definition()
        print sub.my_abstract_method()
