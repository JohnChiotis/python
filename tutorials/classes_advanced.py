class Baseclass(object):
     pass

def echo(self, msg):
    if isinstance(self, Baseclass):
        print msg

# create a class using type
sub = type('Subclass', (Baseclass,), {'echo': echo})()
sub.echo('hello')

# instance and type of a class object
print 'Subclass is instance of Baseclass: %s' % isinstance(sub, Baseclass)
print 'Subclass is type of Baseclass: %s' % (type(sub)==type(Baseclass()))


class A(object):
    """Normal code execution"""
    val = 0
    
    #0 -> 9
    for _ in xrange(10):
        val += 1
    print 'val: %d' % (val)
    
    print 'local scope: %s' % locals()
    
    del val
    try:
        print 'val: %d' % (val)
    except NameError as exc:
        print 'ERROR! %s' % (exc)
        print "val in locals: %s" % ('val' in locals())

# access atrribute of a class
print getattr(A, '_'), A.__dict__.get('_')
