class MyIter(object):
    def __init__(self, sequence):
        self._sequence = sequence
        self._counter = 0
	    
    def __iter__(self):
        return self
		
    def next(self):
        try:
            num = self._sequence[self._counter]
            self._counter += 1
            return num
        except IndexError:
            raise StopIteration


if __name__ == '__main__':
    numbers = range(10, 20)
    my_iter = MyIter(numbers)
    for n1, n2 in zip(my_iter, my_iter):
        print n1, n2
