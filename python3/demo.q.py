
'''
tail -f /tmp/q
'''
import q

foo = 1

q(foo)

@q
def func(arg):
    pass

func(1)

q(2+3)

q.d()
