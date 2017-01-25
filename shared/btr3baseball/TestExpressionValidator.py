from __future__ import print_function
from ExpressionValidator import ExpressionValidator, Atom
import unittest

class TestExpressionValidator(unittest.TestCase):

    def createSimpleValidator(self):
        fdata = [ {'name': 'hi', 'argc': 2} ]
        cdata = [{ 'name': 'HR', 'type': 'N' }, {'name': 'playerId', 'type': 'S'}]
        return ExpressionValidator(funcs = fdata, cols = cdata)

    def helper_testString(self, ex):
        validator = self.createSimpleValidator()
        result = validator.validateExpression(ex)
        print('{} => {}'.format(ex, result))

    def testInteger(self):
        self.helper_testString("2")

    def testFloat(self):
        self.helper_testString("3.14")

ee = [
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

if __name__ == '__main__':
    unittest.main()
