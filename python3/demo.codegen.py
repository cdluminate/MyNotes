'''
codegen
'''

for i in range(10):
    locals()['a{}'.format(i)] = i
print(locals())
def genSumExpr(sl):
    print(sl)
    if len(sl)==0:
        return '0'
    elif len(sl)==1:
        return '{}'.format(sl[0])
    else:
        return '{}+{}'.format(sl[0], genSumExpr(sl[1:]))
symbols = [ 'a{}'.format(i) for i in range(10) ]
print(symbols)
expr = genSumExpr(symbols)
print(expr)
s = eval(expr)
print(s)
