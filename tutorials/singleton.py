class Singleton(type):
    instances = {}
    def __call__(self, *a, **k):
        if self.__name__ not in Singleton.instances:
            Singleton.instances[self.__name__] = type.__call__(self, *a, **k)
        return Singleton.instances[self.__name__]


class Instance(object):
    __metaclass__ = Singleton

    def __init__(self, var):
        print "Init: setting var to: %s" % var
        self.var = var


class Singleton2(object):
    instances = {}
    def __new__(cls, *a, **k):
        if cls.__name__ not in Singleton.instances:
            Singleton.instances[cls.__name__] = object.__new__(cls, *a, **k)
        return Singleton.instances[cls.__name__]


class Instance2(Singleton2):
    def __init__(self, var):
        print "Init: setting var to: %s" % var
        self.var = var


if __name__ == '__main__':
    print "First way"
    inst1 = Instance('first')
    inst2 = Instance('second')
    print 'Instances same:', inst1 is inst2
    print 'Vars:', inst1.var, inst2.var
    
    print "\nSecond way"
    inst1 = Instance2('first')
    inst2 = Instance2('second')
    print 'Instances same:', inst1 is inst2
    print 'Vars:', inst1.var, inst2.var
