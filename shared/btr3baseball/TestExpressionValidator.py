from __future__ import print_function
from ExpressionValidator import (
    ExpressionValidator,
    Atom, 
    UnknownColumnException,
    ColumnTypeMismatchException,
    UnknownFunctionException,
    FunctionArgumentCountMismatchException
)

import unittest

class TestExpressionValidator(unittest.TestCase):

    def createSimpleValidator(self):
        fdata = [ {'name': 'hi', 'argc': 2} ]
        cdata = [{ 'name': 'HR', 'type': 'N' }, {'name': 'playerId', 'type': 'S'}]
        return ExpressionValidator(funcs = fdata, cols = cdata)

    def helper_testString(self, ex):
        validator = self.createSimpleValidator()
        result = validator.validateExpression(ex)
        #print('{} => {}'.format(ex, result))
        return result

    def helper_testString_Exception(self, ex, exc):
        with self.assertRaises(exc):
            self.helper_testString(ex)

    def helper_assertAstTypeAndNext(self, ast, typeName, attrNext):
        self.assertEqual(typeName, ast.__class__.__name__)
        self.assertTrue(hasattr(ast, attrNext))
        return ast.__getattribute__(attrNext)

    def helper_assertAstTypeAndValue(self, ast, typeName, attr, attrVal):
        self.assertEqual(typeName, ast.__class__.__name__)
        self.assertTrue(hasattr(ast, attr))
        self.assertEqual(attrVal, ast.__getattribute__(attr))

    def testInteger(self):
        result = self.helper_testString("2")
        res = self.helper_assertAstTypeAndNext(result.ast, "Expr", 'value')
        res = self.helper_assertAstTypeAndNext(res, "NumExpr", "lterm")
        res = self.helper_assertAstTypeAndNext(res, "Term", "lfactor")
        res = self.helper_assertAstTypeAndNext(res, "Factor", "latom")
        self.helper_assertAstTypeAndValue(res, "Atom", "negate", False)
        self.helper_assertAstTypeAndValue(res, "Atom", "value", '2')

    def testFloat(self):
        result = self.helper_testString("3.14")
        res = self.helper_assertAstTypeAndNext(result.ast, "Expr", 'value')
        res = self.helper_assertAstTypeAndNext(res, "NumExpr", "lterm")
        res = self.helper_assertAstTypeAndNext(res, "Term", "lfactor")
        res = self.helper_assertAstTypeAndNext(res, "Factor", "latom")
        self.helper_assertAstTypeAndValue(res, "Atom", "negate", False)
        self.helper_assertAstTypeAndValue(res, "Atom", "value", '3.14')

    def testString(self):
        result = self.helper_testString("'Hey'")
        res = self.helper_assertAstTypeAndNext(result.ast, "Expr", 'value')
        self.helper_assertAstTypeAndValue(res, "Str", "value", 'Hey')

    def testNegativeInt(self):
        result = self.helper_testString("-2")
        res = self.helper_assertAstTypeAndNext(result.ast, "Expr", 'value')
        res = self.helper_assertAstTypeAndNext(res, "NumExpr", "lterm")
        res = self.helper_assertAstTypeAndNext(res, "Term", "lfactor")
        res = self.helper_assertAstTypeAndNext(res, "Factor", "latom")
        self.helper_assertAstTypeAndValue(res, "Atom", "negate", True)
        self.helper_assertAstTypeAndValue(res, "Atom", "value", '2')

    def testMult(self):
        result = self.helper_testString("2*3")
        res = self.helper_assertAstTypeAndNext(result.ast, "Expr", 'value')
        res = self.helper_assertAstTypeAndNext(res, "NumExpr", "lterm")

        self.helper_assertAstTypeAndValue(res, "Term", "op", "*")
        leftres = self.helper_assertAstTypeAndNext(res, "Term", "lfactor")
        rightres = self.helper_assertAstTypeAndNext(res, "Term", "rterm")

        res = self.helper_assertAstTypeAndNext(leftres, "Factor", "latom")
        self.helper_assertAstTypeAndValue(res, "Atom", "negate", False)
        self.helper_assertAstTypeAndValue(res, "Atom", "value", '2')

        res = self.helper_assertAstTypeAndNext(rightres, "Term", "lfactor")
        res = self.helper_assertAstTypeAndNext(res, "Factor", "latom")
        self.helper_assertAstTypeAndValue(res, "Atom", "negate", False)
        self.helper_assertAstTypeAndValue(res, "Atom", "value", '3')

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
        self.helper_testString_Exception("$('BAD')", UnknownColumnException)

    def testColumnTypeFail(self):
        self.helper_testString_Exception("2 * $('playerId')", ColumnTypeMismatchException)

    def testFuncNameFail(self):
        self.helper_testString_Exception("bad(2)", UnknownFunctionException)

    def testFuncArgcFail(self):
        self.helper_testString_Exception("hi(2)", FunctionArgumentCountMismatchException)

if __name__ == '__main__':
    unittest.main()
