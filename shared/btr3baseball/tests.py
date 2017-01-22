from __future__ import print_function
from ExpressionValidator import ExpressionValidator, Atom
import unittest

vv = ExpressionValidator()

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
] 

check = lambda a: (print(a))
for ex in ee:
    result = vv.parseExpression(ex)
    print('{} => {}'.format(ex, result))
    vv.crawlTree(result.ast, Atom, check)
