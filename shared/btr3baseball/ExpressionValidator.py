from __future__ import print_function
from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas,ParseException


# Grammar and parsing here adapted from public pyparsing examples:
#   http://pyparsing.wikispaces.com/file/view/fourFn.py
#   https://sourceforge.net/p/pyparsing/mailman/message/28157062
class ExpressionValidator:
    def __init__(self):
        point = Literal( "." )
        fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) )
        quote = Literal("'")
        comma = Literal(",").suppress()
        ident = Word(alphas)
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" )
        rpar  = Literal( ")" )
        colmarker = Literal('$')
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )

        numexpr = Forward()
        term = Forward()
        factor = Forward()
        str_const = ( quote + ident + quote ).setParseAction(Str)
        col = ( colmarker + lpar + str_const + rpar ).setParseAction(Col)
        func = ( ident + lpar + Optional( numexpr + ZeroOrMore( (comma + numexpr) ) ) + rpar ).setParseAction(Func)
        atom = ( Optional('-') + ( ( fnumber | func | col ) | ( lpar + numexpr + rpar ) ) ).setParseAction(Atom)
        factor <<  ( ( atom + expop + factor ) | atom ).setParseAction(Factor)
        term << ( ( factor + multop + term ) | factor ).setParseAction(Term)
        numexpr << ( ( term + addop + numexpr ) | term ).setParseAction(NumExpr)
        expr = ( numexpr | str_const ).setParseAction(Expr)
        self.grammar = expr

    def parseExpression(self, strEx):
        try:
            results = self.grammar.parseString(strEx, parseAll=True)
            t = results.dump()
            a = results.asList()
            return ExpressionValidatorResult(expression = strEx, tokens = t, ast = a[0] )
        except ParseException as e:
            return ExpressionValidatorResult(expression = strEx, exception = e)

    def crawlTree(self, ast, checkType, checkFunc):
        for k, v in ast.__dict__.items():
            if isinstance(v , ASTNode) :
                if type(v) == checkType:
                    checkFunc(v)
                self.crawlTree(v, checkType, checkFunc)

class ExpressionValidatorResult:
    def __init__(self, expression = None, tokens = None, ast = None, exception = None):
        self.expression = expression
        self.tokens = tokens
        self.ast = ast
        if exception != None:
            self.message = str(exception)
            self.location = exception.loc
    def __str__(self):
        if self.tokens != None:
            return self.tokens.__str__()
        if self.message != None:
            return 'In expression "{}": {}'.format(self.expression, self.message)

class ASTNode(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.assignFields()
    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)
    __repr__ = __str__

class Col(ASTNode):
    def assignFields(self):
        self.name = self.tokens[2]
        del self.tokens

class Func(ASTNode):
    def assignFields(self):
        self.name = self.tokens[0]
        self.argList = self.tokens[2:-1]
        del self.tokens

class Str(ASTNode):
    def assignFields(self):
        self.value = self.tokens[1]
        del self.tokens

class Atom(ASTNode):
    def assignFields(self):
        self.negate = False
        if (self.tokens[0] == '-'):
            self.negate = True
            self.value = self.tokens[1:]
        else:
            self.value = self.tokens

        if (self.value[0] == '('):
            self.value = self.value[1]
        else:
            self.value = self.value[0]
        del self.tokens

class Factor(ASTNode):
    def assignFields(self):
        self.latom = self.tokens[0]
        if (len(self.tokens) > 1):
            self.exponent = self.tokens[2]
        del self.tokens

class Term(ASTNode):
    def assignFields(self):
        self.lfactor = self.tokens[0]
        if (len(self.tokens) > 1):
            self.op = self.tokens[1]
            self.rterm = self.tokens[2]
        del self.tokens

class NumExpr(ASTNode):
    def assignFields(self):
        self.lterm = self.tokens[0]
        if (len(self.tokens) > 1):
            self.op = self.tokens[1]
            self.rexpr = self.tokens[2]
        del self.tokens

class Expr(ASTNode):
    def assignFields(self):
        self.value = self.tokens[0]
        del self.tokens

