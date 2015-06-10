class Dog(object):
    def __init__(self):
        print 'Dog call'
        super(Dog, self).__init__()
        print 'Dog called'
        self.voice = 'bark'

    def shout(self):
        print 'bark', self.voice


class Duck(object):
    def __init__(self):
        print 'Duck call'
        super(Duck, self).__init__()
        print 'Duck called'
        self.voice = 'quack'
        self.fly = True

    def shout(self):
        print 'quack', self.voice


class Shout(object):
    def __init__(self):
        print 'Shout call'
        super(Shout, self).__init__()
        print 'Shout called'

    def shout(self):
        print 'SHOUT!', self.voice


class Creature(Shout, Dog, Duck):
    def __init__(self):
        print 'Creature call'
        super(Creature, self).__init__()
        print 'Creature called'


if __name__ == '__main__':
    c = Creature()
    print 'Instance ready!'
    c.shout()
    print 'Can fly:', c.fly

    # Call init sequence:
    #     Creature -> Shout -> Dog -> Duck -> Dog -> Shout -> Creature
    # Terminal output:
    #     SHOUT! bark
    #     Can fly: True
