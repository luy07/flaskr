

class Tun(object):
    def __call__(self, *args, **kwargs):
        print('__call__ method invoked')
    def sayHello(self):
        print('hello')

t=Tun((),{})

t.sayHello()