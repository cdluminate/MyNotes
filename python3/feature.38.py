#!/usr/bin/python3.8

# warlus
if (i := 1) > 0:
    print('the warlus operator')

# positional-only
def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)

# f-string
a = 'test string'
b = 3.1415
print(f'{a=} {b=:.1f}')
