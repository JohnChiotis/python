class MyObj(object):
    def __init__(self):
        self._timeout = 30
    
    @property 
    def timeout(self):
        return self._timeout
     
    @timeout.getter
    def timeout(self):
        return 'timeout[%s]' % self._timeout

    @timeout.setter 
    def timeout(self, value):
        print 'setting timeout value: %s' % value
        self._timeout = value

		
if __name__ == '__main__':
    obj = MyObj()
    print obj.timeout
    obj.timeout = 3
    print obj.timeout
