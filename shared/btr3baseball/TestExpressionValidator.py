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
        return result

    def testInteger(self):
        result = self.helper_testString("2")

    def testFloat(self):
        result = self.helper_testString("3.14")

    def testString(self):
        result = self.helper_testString("'Hey'")

    def testNegativeInt(self):
        result = self.helper_testString("-2")

    def testMult(self):
        result = self.helper_testString("2*3")

    def testMultAndAdd(self):
        result = self.helper_testString("2*3 + 5*4")       

    def testMultMany(self):
        result = self.helper_testString("2*3*4")

    def testExponent(self):
        result = self.helper_testString("5^2")

    def testFuncTwoArgs(self):
        result = self.helper_testString("hi(2,3)")
    
    def testColumn(self):
        result = self.helper_testString("$('HR')")

    def testMultWithColumn(self):
        result = self.helper_testString("2 * $('HR')")

    def testParen(self):
        result = self.helper_testString("(2 + 5) * 3")

    def testColumnFail(self):
        result = self.helper_testString("$('BAD')")

    def testColumnTypeFail(self):
        result = self.helper_testString("2 * $('playerId')")

    def testFuncNameFail(self):
        result = self.helper_testString("bad(2)")

    def testFuncArgcFail(self):
        result = self.helper_testString("hi(2)")

if __name__ == '__main__':
    unittest.main()
