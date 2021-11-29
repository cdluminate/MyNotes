'''
SymPy demonstration
http://docs.sympy.org/latest/tutorial/intro.html
'''
import sympy as sp
sp.init_printing(use_unicode=True)

print(sp.sqrt(3))
print(sp.sqrt(8))

x, y = sp.symbols('x y')
expr = x + 2*y + 1
print(expr)

print(sp.expand(x * expr))
print(sp.factor(sp.expand(x * expr)))

x, t, z, nu = sp.symbols('x t z nu')
print(sp.diff(sp.sin(x)*sp.exp(x), x))
print(sp.integrate(sp.exp(x)*sp.sin(x) + sp.exp(x)*sp.cos(x), x))

print(sp.integrate(sp.sin(x**2), (x, -sp.oo, sp.oo)))

print(sp.limit(sp.sin(x)/x, x, 0))

print(sp.solve(x**2 - 2, x))
y = sp.Function('y')
print(sp.solve(sp.Eq(y(t).diff(t, t) - y(t), sp.exp(t)), y(t)))

A = sp.Matrix([[1,2],[2,2]])
print(A.eigenvals())
print(sp.latex(A.eigenvals()))
