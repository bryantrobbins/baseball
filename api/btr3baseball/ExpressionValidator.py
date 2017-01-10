from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas,ParseException

point = Literal( "." )
fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) )
const = Literal( "CONST").suppress()
quote = Literal("'").suppress()
ident = Word(alphas, alphas+nums)
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
num_const = const + lpar + fnumber + rpar
str_const = const + lpar + quote + ident + quote + rpar
addop  = plus | minus
multop = mult | div
expop = Literal( "^" )

expr = Forward()
atom = num_const | str_const
factor = Forward()
factor << atom
term = str_const | factor + ZeroOrMore( ( multop + factor ))
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

# Some quick tests (temp)
vv = ExpressionValidator()
ee = ["CONST('JOHNNY')", "CONST(2) * CONST('HR')"]

for ex in ee:
    result = vv.parseExpression(ex)
    print('{} => {}'.format(ex, result))
