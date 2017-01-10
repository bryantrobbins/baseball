from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas,ParseException

point = Literal( "." )
fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) )
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
addop  = plus | minus
multop = mult | div
expop = Literal( "^" )

expr = Forward()
atom = fnumber
factor = Forward()
factor << atom
term = factor + ZeroOrMore( ( multop + factor ))
expr << term + ZeroOrMore( ( addop + term ))

class ExpressionValidator:
    def __init__(self):
        self.grammar = expr

    def parseExpression(self, strEx):
        try:
            results = self.grammar.parseString(strEx, parseAll=True).dump()
            return ExpressionValidatorResult(expression = strEx, tokens = results)
        except ParseException as e:
            return ExpressionValidatorResult(expression = strEx, exception = e)

class ExpressionValidatorResult:
    def __init__(self, expression = None, tokens = None, exception = None):
        self.expression = expression
        self.tokens = tokens
        if exception != None:
            self.message = str(exception)
            self.location = exception.loc
    def __str__(self):
        if self.tokens != None:
            return self.tokens.__str__()
        if self.message != None:
            return 'In expression "{}": {}'.format(self.expression, self.message)

vv = ExpressionValidator()
result = vv.parseExpression("2.3-6")
print(result)
