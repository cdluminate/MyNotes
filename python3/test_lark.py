from lark import Lark, Transformer
import rich
console = rich.get_console()
import numpy as np
import functools as ft

grammar = r'''
?start: expression*
?expression: prob idx idx NEWLINE*
?prob: NUMBER -> float
?idx: INT -> int
%import common.NEWLINE
%import common.NUMBER
%import common.WS_INLINE
%import common.INT
%import common.FLOAT
%ignore WS_INLINE
'''

parser = Lark(grammar)
#ast = parser.parse('')
ast = parser.parse('1.0 1 1\n \n 1 2 2 \n 1 0 0 ')
console.print(ast)

def run_ast(ast, ctx):
    if ast.data == 'int':
        return int(ast.children[0])
    elif ast.data == 'float':
        return float(ast.children[0])
    elif ast.data == 'expression':
        p, i, j = map(ft.partial(run_ast, ctx=ctx), ast.children[:3])
        console.log('E[%d,%d] <- %.1f' % (i, j, p))
        ctx[i, j] = p
    elif ast.data == 'start':
        for x in ast.children:
            run_ast(x, ctx)

E = np.zeros((3,3))
print('before', E)
run_ast(ast, E)
print('after', E)


class Runner(Transformer):
    def __init__(self, ctx):
        self.ctx = ctx
    def __str__(self):
        return 'Runner: ' + str(self.ctx.ravel())
    def int(self, args):
        return int(args[0])
    def float(self, args):
        return float(args[0])
    def expression(self, args):
        p, i, j = args[:3]
        self.ctx[i, j] = p

runner = Runner(np.zeros((3,3)))
print(runner)
runner.transform(ast)
print(runner)
print(runner.ctx)
