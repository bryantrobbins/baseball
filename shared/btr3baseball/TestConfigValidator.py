from __future__ import print_function
from ExpressionValidator import ExpressionValidator, Atom
import unittest

fdata = [ {'name': 'hi', 'argc': 2} ]
cdata = [{ 'name': 'HR', 'type': 'N' }, {'name': 'playerId', 'type': 'S'}]
vv = ExpressionValidator(funcs = fdata, cols = cdata)

ee = [
    "2",
    "3.14",
    "'Hey'",
    "-2",
    "2*3",
    "2*3 + 5*4",
    "2*3*4",
    "5^2",
    "hi(2,3)",
    "$('HR')",
    "2 * $('HR')",
    "2 * 3 * $('HR')",
    "(2 + 5) * 3",
    "$('BAD')",
    "bad(2)",
    "2 * $('playerId')",
    "hi(2)",
] 

for ex in ee:
    result = vv.validateExpression(ex)
    print('{} => {}'.format(ex, result))
