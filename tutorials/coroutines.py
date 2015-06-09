def pattern_filter(pattern):
    print '%sCoroutine Starts' % (' '*4)
    try:
        while True:
            line = (yield)
            if pattern in line:
                yield line
            else:
                yield None
    except GeneratorExit:
        print '%sCoroutine Exits\n' % (' '*4)

def grep(pattern, lines):
    my_filter = pattern_filter(pattern)
    for line in lines:
        my_filter.next()
        result = my_filter.send(line)
        if result:
            yield '%s%s' % (' '*4, result)
    my_filter.throw(GeneratorExit)


if __name__ == '__main__':
    lines = ['Java is not bad',
             'Java is nice',
             'but Python rocks!']

    print "Java filter:"
    for line in grep('Java', lines):
        print line
        
    print "Python filter:"
    for line in grep('Python', lines):
        print line
