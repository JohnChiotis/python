def get_all_permutations(arraylist, idx=None):
    """Generator that yields all permutations of an input arraylist."""
    if idx is None:
        idx = len(arraylist)
    if idx == 0:
        yield []
    elif idx == 1:
        yield [arraylist[-idx]]
    else:
        for perm in get_all_perms(arraylist, idx=idx-1):
            for i in xrange(0, len(perm)+1):
                new_perm = perm[:]
                new_perm.insert(i, arraylist[-idx])
                yield new_perm

def simple_generator(iterable):
    for item in iterable:
	    yield item

		
if __name__ == '__main__':
    perm_generator = get_all_permutations(['h', 'a', 't'])
    print "Get permutations: %s" % (perm_generator)
    for p in simple_generator(perm_generator):
        print p
