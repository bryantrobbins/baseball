from __future__ import print_function
from ExpressionValidator import ExpressionValidator, Atom
import unittest

vv = ExpressionValidator(funcs = ['hi'], cols = ['HR'])

ee = [
    "2",
    "3.14",
    "'Hey'",
    "-2",
    "2*3",
    "2*3 + 5*4",
    "2*3*4",
    "5^2",
    "hi(2)",
    "hi(2,3)",
    "$('HR')",
    "2 * $('HR')",
    "2 * 3 * $('HR')",
    "(2 + 5) * 3",
    "$('BAD')",
] 

for ex in ee:
    result = vv.validateExpression(ex)
    print('{} => {}'.format(ex, result))
