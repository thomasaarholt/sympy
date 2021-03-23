from sympy import lambdify, Sum, sqrt, log
from sympy.abc import x, i, a, b
from sympy.codegen.numpy_nodes import logaddexp
from sympy.codegen.cfunctions import log10
from sympy.printing.numpy import CuPyPrinter

from sympy.testing.pytest import skip
from sympy.external import import_module

cp = import_module('cupy')

def test_cupy_print():
    prntr = CuPyPrinter()
    assert prntr.doprint(logaddexp(a, b)) == 'cupy.logaddexp(a, b)'
    assert prntr.doprint(sqrt(x)) == 'cupy.sqrt(x)'
    assert prntr.doprint(log(x)) == 'cupy.log(x)'
    assert prntr.doprint("acos(x)") == 'cupy.arccos(x)'
    assert prntr.doprint("exp(x)") == 'cupy.exp(x)'
    assert prntr.doprint("Abs(x)") == 'abs(x)'

def test_not_cupy_print():
    prntr = CuPyPrinter()
    assert "Not supported" in prntr.doprint("abcd(x)")

def test_sum():
    if not cp:
        skip("CuPy not installed")

    s = Sum(x ** i, (i, a, b))
    f = lambdify((a, b, x), s, 'cupy')

    a_, b_ = 0, 10
    x_ = cp.linspace(-1, +1, 10)
    assert cp.allclose(f(a_, b_, x_), sum(x_ ** i_ for i_ in range(a_, b_ + 1)))

    s = Sum(i * x, (i, a, b))
    f = lambdify((a, b, x), s, 'numpy')

    a_, b_ = 0, 10
    x_ = cp.linspace(-1, +1, 10)
    assert cp.allclose(f(a_, b_, x_), sum(i_ * x_ for i_ in range(a_, b_ + 1)))
