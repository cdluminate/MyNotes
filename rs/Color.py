#!/usr/bin/python3
'''
ANSI Terminal Colorization Module: 256 Colors
Copyright (C) 2019 M. Zhou <lumin@debian.org>
'''
import sys
import functools


def colorize(color: str, *msg):
    '''
    Normal Color
    '''
    return f'\x1b[{color}m' + ' '.join(str(x) for x in msg) + '\x1b[m'


# Red 31 / 41
fgR = functools.partial(colorize, '31')
bgR = functools.partial(colorize, '41')
fgRed = functools.partial(colorize, '38;5;196')
bgRed = functools.partial(colorize, '48;5;196')

# Green 32 / 42
fgG = functools.partial(colorize, '32')
bgG = functools.partial(colorize, '42')
fgGreen = functools.partial(colorize, '38;5;40')
bgGreen = functools.partial(colorize, '48;5;40')

# Yellow 33 / 43
fgY = functools.partial(colorize, '33')
bgY = functools.partial(colorize, '43')
fgYellow = functools.partial(colorize, '38;5;220')
bgYellow = functools.partial(colorize, '48;5;220')

# Blue 34 / 44
fgB = functools.partial(colorize, '34')
bgB = functools.partial(colorize, '44')
fgBlue = functools.partial(colorize, '38;5;39')
bgBlue = functools.partial(colorize, '48;5;39')

# Violet 35 / 45
fgV = functools.partial(colorize, '35')
bgV = functools.partial(colorize, '45')
fgViolet = functools.partial(colorize, '38;5;93')
bgViolet = functools.partial(colorize, '48;5;93')

# Cyan 36 / 46
fgC = functools.partial(colorize, '36')
bgC = functools.partial(colorize, '46')
fgCyan = functools.partial(colorize, '38;5;51')
bgCyan = functools.partial(colorize, '48;5;51')

# Other colors
fgOrange = functools.partial(colorize, '38;5;208')
bgOrange = functools.partial(colorize, '48;5;208')
fgMagenta = functools.partial(colorize, '38;5;161')
bgMagenta = functools.partial(colorize, '48;5;161')
fgAqua = functools.partial(colorize, '38;5;45')
bgAqua = functools.partial(colorize, '48;5;45')


if __name__ == '__main__':
    def test(f1, f2, f3, f4):
        print(f1('test'), f2('test'), f3('test'), f4('test'))
    test(fgR, bgR, fgRed, bgRed)
    test(fgG, bgG, fgGreen, bgGreen)
    test(fgY, bgY, fgYellow, bgYellow)
    test(fgB, bgB, fgBlue, bgBlue)
    test(fgV, bgV, fgViolet, bgViolet)
    test(fgC, bgC, fgCyan, bgCyan)
    print(fgOrange('test'), bgOrange('test'))
    print(fgMagenta('test'), bgMagenta('test'))
    print(fgAqua('test'), bgAqua('test'))
