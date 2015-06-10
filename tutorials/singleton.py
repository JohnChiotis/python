class Singleton(type):
    instances = {}
    def __call__(cls, *a, **k):
        if cls.__name__ not in Singleton.instances:
            Singleton.instances[cls.__name__] = type.__call__(cls, *a, **k)
        return Singleton.instances[cls.__name__]


class Instance(object):
    __metaclass__ = Singleton

    def __init__(self, var):
        print "Init: setting var to: %s" % var
        self.var = var


if __name__ == '__main__':
    inst1 = Instance('first')
    inst2 = Instance('second')
    print 'Instances:', inst1, inst2
    print 'Vars:', inst1.var, inst2.var
